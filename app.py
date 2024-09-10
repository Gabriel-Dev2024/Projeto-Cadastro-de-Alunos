import customtkinter as ctk
from customtkinter import *
from tkinter import messagebox, END
import bcrypt
import sqlite3

class DB_Usuarios():
    def conecta_db(self):

        # Conecta ao banco de dados SQLite ou cria um novo se não existir
        self.conn = sqlite3.connect('Usuarios.db')
        self.cursor = self.conn.cursor()
        print('Banco de dados conectado com sucesso!')

    def desconecta_db(self):

        # Fecha a conexão com o banco de dados
        self.conn.close()

    def cria_tabela(self):

        # Cria a tabela Usuarios se ela não existir no banco de dados
        self.conecta_db()

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Usuarios(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                username TEXT NOT NULL UNIQUE,
                senha TEXT NOT NULL,
                telefone TEXT
            )
        """)
        self.conn.commit()
        print('Tabela criada com sucesso!')
        self.desconecta_db()

class Application(DB_Usuarios):
    def __init__(self):

        self.janela = ctk.CTk()
        self.tema()
        self.tela()
        self.tela_login()
        self.cria_tabela()
        self.janela.mainloop()

    def tema(self):
        # Define o tema da tela
        ctk.set_appearance_mode('dark')
        ctk.set_default_color_theme('blue')

    def tela(self):
        # Configurações da tela principal
        self.janela.geometry('700x500')
        self.janela.title('Sistema de Cadastro de Alunos')
        self.janela.resizable(False, False) # Para impedir o usuario de aumentar e diminiur a senha

    def tela_login(self):

        # Cria o frame de login
        self.login_frame = ctk.CTkFrame(master=self.janela, width=450, height=500, fg_color='#0B42EC')
        self.login_frame.pack()

        # Widgets do frame de login
        label = ctk.CTkLabel(master=self.login_frame, text='Página de Login', font=('Arial', 24))
        label.place(x=150, y=20)

        self.username_entry = ctk.CTkEntry(master=self.login_frame, placeholder_text='Nome do Usuário ou Email', width=300, font=('Arial', 16))
        self.username_entry.place(x=85, y=120)
        label1 = ctk.CTkLabel(master=self.login_frame, text='*O campo de Usuário é OBRIGATÓRIO', text_color='white', font=('Arial', 12))
        label1.place(x=85, y=160)

        self.password_entry = ctk.CTkEntry(master=self.login_frame, placeholder_text='Senha do Usuário', width=300, font=('Arial', 16), show='*')
        self.password_entry.place(x=85, y=210)
        label2 = ctk.CTkLabel(master=self.login_frame, text='*O campo de Senha é OBRIGATÓRIO', text_color='white', font=('Arial', 12))
        label2.place(x=85, y=250)

        # CheckBox para mostrar e ocultar a senha
        self.show_check = ctk.CTkCheckBox(master=self.login_frame, text='Mostrar senha', width=100, command=self.show_password)
        self.show_check.place(x=300, y=253)

        # Botão de Login
        login_button = ctk.CTkButton(master=self.login_frame, text='Login', width=300, command=self.pagina_principal) # Colocar a função de login
        login_button.place(x=85, y=300)

        register_span = ctk.CTkLabel(master=self.login_frame, text='Recuperar senha', width=155)
        register_span.place(x=80, y=340)

        # Botão de Cadastro
        register_button = ctk.CTkButton(master=self.login_frame, text='Cadastre-se', width=155, fg_color='green', hover_color='#2D9334', command=self.tela_register)
        register_button.place(x=230, y=340)

    def login(self):

        # Verifica se os dados do usuario é válido
        if self.validator_login():
            username_or_email = self.username_entry.get().strip()
            password = self.password_entry.get().strip()

            # Usa a função check_usuarios para ver se o usuario esta cadastrado e se pode fazer o login
            if self.check_usuarios(username_or_email, password):
                messagebox.showinfo(title='Estado de Login', message='Login Feito com Sucesso')
                print(f'{username_or_email} Login feito com sucesso')
                self.clear_entry_login()
                self.pagina_principal()
            else:
                messagebox.showerror(title='ERRO', message='Nome de Usuario ou Senha Incorretos')
                print(f'{username_or_email} Falha ao fazer o Login')

    def check_usuarios(self, username_or_email, password):
        self.conecta_db()

        # Procura a senha e o username_or_email na tabela de usuarios
        self.cursor.execute("""
            SELECT senha FROM Usuarios
            WHERE username = ? OR email = ?""", (username_or_email, username_or_email))
        result = self.cursor.fetchone()
        self.desconecta_db()

        if result:
            self.hashed_password = result[0]
            return self.check_password(password, self.hashed_password)
        return False

    def validator_login(self):

        # Valida se os campos de login foram preenchidos
        username_or_email = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        # Verifica se os campos estão corretos
        if not username_or_email or not password:
            messagebox.showerror(title='ERRO', message='Preencha com seus dados')
            return False
        return True
    


    def tela_register(self):
        # Remove o frame de login
        self.login_frame.pack_forget()

        # Cria o frame de registro
        self.rg_frame = ctk.CTkFrame(master=self.janela, width=450, height=500, fg_color='#0B42EC')
        self.rg_frame.pack()

        label = ctk.CTkLabel(master=self.rg_frame, text='Página de Cadastro', font=('Arial', 24))
        label.place(x=130, y=20)

        self.name_entry_reg = ctk.CTkEntry(master=self.rg_frame, placeholder_text='Nome completo', width=300, font=('Arial', 16))
        self.name_entry_reg.place(x=85, y=80)

        self.email_entry_reg = ctk.CTkEntry(master=self.rg_frame, placeholder_text='Email do Usuário', width=300, font=('Arial', 16))
        self.email_entry_reg.place(x=85, y=120)

        self.username_entry_reg = ctk.CTkEntry(master=self.rg_frame, placeholder_text='Nome do Usuário', width=300, font=('Arial', 16))
        self.username_entry_reg.place(x=85, y=160)

        self.password_entry_reg = ctk.CTkEntry(master=self.rg_frame, placeholder_text='Senha do Usuário', width=300, font=('Arial', 16), show='*')
        self.password_entry_reg.place(x=85, y=200)

        self.cPassword_entry_reg = ctk.CTkEntry(master=self.rg_frame, placeholder_text='Confirma a Senha', width=300, font=('Arial', 16), show='*')
        self.cPassword_entry_reg.place(x=85, y=240)

        self.phone_entry_reg = ctk.CTkEntry(master=self.rg_frame, placeholder_text='Telefone (Opcional)', width=300, font=('Arial', 16))
        self.phone_entry_reg.place(x=85, y=280)

        # CheckBox para Termos de Uso e Política de Privacidade 
        self.termos_e_politicas = ctk.CTkCheckBox(master=self.rg_frame, text='Termos de Usos e Políticas de Privacidade', width=100)
        self.termos_e_politicas.place(x=85, y=320)

        # Botão para Voltar
        back_button = ctk.CTkButton(master=self.rg_frame, text='Voltar', width=145, fg_color='gray', hover_color='#202020', command=self.voltar_login)
        back_button.place(x=85, y=370)

        # Botão para Cadastrar
        save_button = ctk.CTkButton(master=self.rg_frame, text='Cadastrar', width=145, fg_color='green', hover_color='#014B05', command=self.cadastrar_usuarios)
        save_button.place(x=240, y=370)

    def cadastrar_usuarios(self):
        if self.validator_register():
            self.name_cadastro = self.name_entry_reg.get()
            self.email_cadastro = self.email_entry_reg.get()
            self.username_cadastro = self.username_entry_reg.get()
            self.senha_cadastro = self.password_entry_reg.get()
            self.telefone_cadastro = self.phone_entry_reg.get()

            print(f'Usuário {self.username_cadastro} cadastrado com sucesso!')

            self.password_encrypt = self.hash_password(self.senha_cadastro)

            self.conecta_db()

            # Inseri as informações no banco de dados
            self.cursor.execute("""
                INSERT INTO Usuarios (nome, email, username, senha, telefone)
                VALUES (?, ?, ?, ?, ?)""", (self.name_cadastro, self.email_cadastro, self.username_cadastro, self.password_encrypt.decode(), self.telefone_cadastro))
            
            self.conn.commit()
            print('Dados inseridos com sucesso!')
            self.desconecta_db()

            messagebox.showinfo(title='Estado de Cadastro', message='Usuário Cadastrado com Sucesso')

            self.clear_entry_register()
        else:
            messagebox.showerror(title='ERRO', message='Não foi possível cadastrar o usuário.')

            print('Não foi possível cadastrar o usuário.')

    def validator_register(self):
        name = self.name_entry_reg.get().strip()
        email = self.email_entry_reg.get().strip()
        username = self.username_entry_reg.get().strip()
        password = self.password_entry_reg.get().strip()
        cPassword = self.cPassword_entry_reg.get().strip()
        termos = self.termos_e_politicas.get()

        if not name or not username or not email or not password or not cPassword:
            messagebox.showerror(title='ERRO', message='Preencha Todos os Campos')
            return False
        if len(password) < 6:
            messagebox.showerror(title='ERRO', message='A Senha deve ter 6 ou mais Caracteres')
            return False
        if cPassword != password:
            messagebox.showerror(title='ERRO', message='As Senhas devem ser iguais')
            return False
        if not termos:
            messagebox.showerror(title='ERRO', message='Você deve aceitar os termos de usos')
            return False
        return True
    
    def voltar_login(self):
            # Remove o frame de registro
            self.rg_frame.pack_forget()

            # Devolve o frame de login
            self.login_frame.pack()
    

    
    def show_password(self):
        if self.show_check.get():
            self.password_entry.configure(show='')
        else:
            self.password_entry.configure(show='*')

    def clear_entry_login(self):
        self.username_entry.delete(0, END)
        self.password_entry.delete(0, END)

    def clear_entry_register(self):
        self.name_entry_reg.delete(0, END)
        self.email_entry_reg.delete(0, END)
        self.username_entry_reg.delete(0, END)
        self.password_entry_reg.delete(0, END)
        self.cPassword_entry_reg.delete(0, END)
        self.phone_entry_reg.delete(0, END)

    def hash_password(self, password):
        self.password = password.encode()
        self.salt = bcrypt.gensalt()
        return bcrypt.hashpw(self.password, self.salt)
    
    def check_password(self, password, hashed_password):
        if isinstance(hashed_password, str):
            hashed_password = hashed_password.encode('utf-8')
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
        


    def pagina_principal(self):
        self.login_frame.pack_forget()

        self.janela.geometry('1000x900')

        self.pag_principal_frame = ctk.CTkFrame(master=self.janela, width=800, height=900, fg_color='#0B42EC')
        self.pag_principal_frame.pack()

        self.tabview = ctk.CTkTabview(master=self.pag_principal_frame)
        self.tabview.pack(padx=250, pady=330)

        self.tabview.add('Pagina Principal')
        self.tabview.add('Cadastrar Alunos')
        self.tabview.add('Consultar Alunos')

        label1 = ctk.CTkLabel(master=self.tabview.tab('Pagina Principal'), text='Pagina Principal', font=('Arial', 24))
        label1.place(x=100, y=40)


    
    #def pagina_info_pessoais(self):

Application()