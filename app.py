import customtkinter as ctk
from customtkinter import *
from tkinter import messagebox, END
import bcrypt
from DataBase.usuarios_db import DB_Usuarios

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
        ctk.set_appearance_mode('light')

    def tela(self):
        # Configurações da tela principal
        self.janela.geometry('700x500')
        self.janela.title('Sistema de Cadastro de Alunos')
        self.janela.resizable(False, False) # Para impedir o usuario de aumentar e diminiur a senha

    def tela_login(self):

        # Cria o frame de login
        self.login_frame = ctk.CTkFrame(master=self.janela, width=450, height=500, fg_color='#006CBB')
        self.login_frame.pack()

        # Widgets do frame de login
        label = ctk.CTkLabel(master=self.login_frame, text='Página de Login', font=('Arial', 24), text_color='white')
        label.place(x=150, y=40)

        self.username_entry = ctk.CTkEntry(master=self.login_frame, placeholder_text='Nome do Usuário ou Email', width=300, font=('Arial', 16))
        self.username_entry.place(x=85, y=120)
        label1 = ctk.CTkLabel(master=self.login_frame, text='*O campo de Usuário é OBRIGATÓRIO', text_color='white', font=('Arial', 12))
        label1.place(x=85, y=160)

        self.password_entry = ctk.CTkEntry(master=self.login_frame, placeholder_text='Senha do Usuário', width=300, font=('Arial', 16), show='*')
        self.password_entry.place(x=85, y=210)
        label2 = ctk.CTkLabel(master=self.login_frame, text='*O campo de Senha é OBRIGATÓRIO', text_color='white', font=('Arial', 12))
        label2.place(x=85, y=250)

        # CheckBox para mostrar e ocultar a senha
        self.show_check = ctk.CTkCheckBox(master=self.login_frame, text='Mostrar senha', width=100, text_color='white', hover_color='#0159A9', command=self.show_password)
        self.show_check.place(x=300, y=253)

        # Botão de Login
        login_button = ctk.CTkButton(master=self.login_frame, text='Login', width=300, hover_color='#0159A9', font=('Arial', 20), command=self.criar_pagina_principal) # Colocar a função de login
        login_button.place(x=85, y=300)

        register_span = ctk.CTkLabel(master=self.login_frame, text='Recuperar senha', width=155, text_color='white')
        register_span.place(x=80, y=340)

        # Botão de Cadastro
        register_button = ctk.CTkButton(master=self.login_frame, text='Cadastre-se', width=155, fg_color='green', hover_color='#014B05', font=('Arial', 20), command=self.tela_register)
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
                self.criar_pagina_principal('pagina_principal')
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
   
    def show_password(self):
        if self.show_check.get():
            self.password_entry.configure(show='')
        else:
            self.password_entry.configure(show='*')

    def clear_entry_login(self):
        self.username_entry.delete(0, END)
        self.password_entry.delete(0, END)

    def check_password(self, password, hashed_password):
            if isinstance(hashed_password, str):
                hashed_password = hashed_password.encode('utf-8')
            return bcrypt.checkpw(password.encode('utf-8'), hashed_password)




    def tela_register(self):
        # Remove o frame de login
        self.login_frame.pack_forget()

        # Cria o frame de registro
        self.rg_frame = ctk.CTkFrame(master=self.janela, width=450, height=500, fg_color='#006CBB')
        self.rg_frame.pack()

        label = ctk.CTkLabel(master=self.rg_frame, text='Página de Cadastro', font=('Arial', 24), text_color='white')
        label.place(x=130, y=40)

        self.name_entry_reg = ctk.CTkEntry(master=self.rg_frame, placeholder_text='Nome completo', width=300, font=('Arial', 16))
        self.name_entry_reg.place(x=85, y=110)

        self.email_entry_reg = ctk.CTkEntry(master=self.rg_frame, placeholder_text='Email do Usuário', width=300, font=('Arial', 16))
        self.email_entry_reg.place(x=85, y=150)

        self.username_entry_reg = ctk.CTkEntry(master=self.rg_frame, placeholder_text='Nome do Usuário', width=300, font=('Arial', 16))
        self.username_entry_reg.place(x=85, y=190)

        self.password_entry_reg = ctk.CTkEntry(master=self.rg_frame, placeholder_text='Senha do Usuário', width=300, font=('Arial', 16), show='*')
        self.password_entry_reg.place(x=85, y=230)

        self.cPassword_entry_reg = ctk.CTkEntry(master=self.rg_frame, placeholder_text='Confirma a Senha', width=300, font=('Arial', 16), show='*')
        self.cPassword_entry_reg.place(x=85, y=270)

        self.phone_entry_reg = ctk.CTkEntry(master=self.rg_frame, placeholder_text='Telefone (Opcional)', width=300, font=('Arial', 16))
        self.phone_entry_reg.place(x=85, y=310)

        # CheckBox para Termos de Uso e Política de Privacidade
        self.termos_e_politicas = ctk.CTkCheckBox(master=self.rg_frame, text='Termos de Usos e Políticas de Privacidade', width=100, text_color='white', hover_color='#0159A9')
        self.termos_e_politicas.place(x=85, y=350)

        # Botão para Voltar
        back_button = ctk.CTkButton(master=self.rg_frame, text='Voltar', width=145, fg_color='gray', hover_color='#202020', font=('Arial', 20), command=self.voltar_login)
        back_button.place(x=85, y=400)

        # Botão para Cadastrar
        save_button = ctk.CTkButton(master=self.rg_frame, text='Cadastrar', width=145, fg_color='green', hover_color='#014B05', font=('Arial', 20), command=self.cadastrar_usuarios)
        save_button.place(x=240, y=400)

    def cadastrar_usuarios(self):
        if self.validator_register():
            self.name_cadastro = self.name_entry_reg.get()
            self.email_cadastro = self.email_entry_reg.get()
            self.username_cadastro = self.username_entry_reg.get()
            self.senha_cadastro = self.password_entry_reg.get()
            self.telefone_cadastro = self.phone_entry_reg.get()

            self.conecta_db()

            self.cursor.execute("SELECT * FROM Usuarios WHERE username = ? OR email = ?", (self.username_cadastro, self.email_cadastro))
            self.usuario_existente = self.cursor.fetchone()

            if self.usuario_existente:
                messagebox.showerror(title='ERRO', message='Usuário ou Email já existem.')
                print('Usuario ou Email já existem.')
                self.desconecta_db()
                return

            print(f'Usuário {self.username_cadastro} cadastrado com sucesso!')

            self.password_encrypt = self.hash_password(self.senha_cadastro)

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
   
       



    def criar_pagina_principal(self):
        self.login_frame.pack_forget()
        self.janela.geometry('850x650')
        self.side_bar()

        self.pagina_principal_frame = ctk.CTkFrame(master=self.janela, width=700, height=650, fg_color='white', corner_radius=0)
        self.pagina_principal_frame.pack_propagate(0)
        self.pagina_principal_frame.pack(fill='both', expand=True)

        label_pag_principal = ctk.CTkLabel(master=self.pagina_principal_frame, text='Pagina Principal', font=('Arial', 32), text_color='black')
        label_pag_principal.pack(pady=(50, 0))

        label_mensagem = ctk.CTkLabel(master=self.pagina_principal_frame, text='Bem Vindo ao Sistema de Gerenciamento de Alunos!', font=('Arial', 20), text_color='black')
        label_mensagem.pack(pady=(50, 0))




    def criar_cadastrar_alunos(self):
        self.pagina_principal_frame.pack_forget()

        self.pagina_cadastrar_alunos_frame = ctk.CTkFrame(master=self.janela, width=630, height=650, fg_color='white', corner_radius=0)
        self.pagina_cadastrar_alunos_frame.pack_propagate(0)
        self.pagina_cadastrar_alunos_frame.pack(fill='both', expand=True)

        label_title = ctk.CTkLabel(master=self.pagina_cadastrar_alunos_frame, text='Pagina de Cadastro de Alunos', font=('Arial', 32), text_color='black')
        label_title.pack(pady=(50, 0))

        button_cadastrar = ctk.CTkButton(master=self.pagina_cadastrar_alunos_frame, text='Cadastrar Aluno', hover_color='#0159A9', font=('Arial', 20), anchor='w', command=self.informacoes_pessoais)
        button_cadastrar.pack(pady=(50, 0))

        button_voltar = ctk.CTkButton(master=self.pagina_cadastrar_alunos_frame, width=70, text='Voltar', fg_color='gray', hover_color='#202020', font=('Arial', 20), command=self.voltar_do_cadastro)
        button_voltar.pack(pady=(50, 0))

    def informacoes_pessoais(self):
        self.pagina_cadastrar_alunos_frame.pack_forget()
        self.side_bar_pag.pack_forget()

        self.informacoes_pessoais_frame = ctk.CTkFrame(master=self.janela, width=550, height=670, fg_color='#006CBB')
        self.informacoes_pessoais_frame.pack_propagate(0)
        self.informacoes_pessoais_frame.pack()

        label_title = ctk.CTkLabel(master=self.informacoes_pessoais_frame, text='Informações Pessoais', font=('Arial', 32), text_color='white')
        label_title.pack(pady=(40, 0))

        self.nome_completo_aluno = ctk.CTkEntry(master=self.informacoes_pessoais_frame, placeholder_text='Nome Completo do Aluno', width=400, font=('Arial', 16))
        self.nome_completo_aluno.pack(anchor='center', pady=(60, 0))

        self.data_nascimento = ctk.CTkEntry(master=self.informacoes_pessoais_frame, placeholder_text='Data de Nascimento (Ex: 00/00/0000)', width=400, font=('Arial', 16))
        self.data_nascimento.pack(anchor='center', pady=(20, 0))

        self.genero = ctk.CTkComboBox(master=self.informacoes_pessoais_frame, values=['Masculino', 'Feminino'])
        self.genero.pack(anchor='center', pady=(20, 0))

        self.cpf = ctk.CTkEntry(master=self.informacoes_pessoais_frame, placeholder_text='CPF (Ex: 000.000.000-00)', width=400, font=('Arial', 16))
        self.cpf.pack(anchor='center', pady=(20, 0))

        self.rg = ctk.CTkEntry(master=self.informacoes_pessoais_frame, placeholder_text='RG (Ex: 00.000.000-00)', width=400, font=('Arial', 16))
        self.rg.pack(anchor='center', pady=(20, 0))

        self.nacionalidade = ctk.CTkEntry(master=self.informacoes_pessoais_frame, placeholder_text='Nacionalidade', width=400, font=('Arial', 16))
        self.nacionalidade.pack(anchor='center', pady=(20, 0))

        self.naturalidade = ctk.CTkEntry(master=self.informacoes_pessoais_frame, placeholder_text='Naturalidade (Cidade/Estado)', width=400, font=('Arial', 16))
        self.naturalidade.pack(anchor='center', pady=(20, 0))

        self.estado_civil = ctk.CTkComboBox(master=self.informacoes_pessoais_frame, values=['Solteiro', 'Casado', 'Divorciado', 'Viúvo'])
        self.estado_civil.pack(anchor='center', pady=(20, 0))

        button_proxima_pagina = ctk.CTkButton(master=self.informacoes_pessoais_frame, text='Próxima Página', text_color='white', fg_color='green', hover_color='#014B05', font=('Arial', 20), command=self.reconhecimento)
        button_proxima_pagina.place(x=280, y=550)

        button_voltar = ctk.CTkButton(master=self.informacoes_pessoais_frame, width=120, text='Voltar', fg_color='gray', hover_color='#202020', font=('Arial', 20))
        button_voltar.place(x=130, y=550)

    def reconhecimento(self):
        self.informacoes_pessoais_frame.pack_forget()
        
        self.reconhecimento_frame = ctk.CTkFrame(master=self.janela, width=550, height=670, fg_color='#006CBB')
        self.reconhecimento_frame.pack_propagate(0)
        self.reconhecimento_frame.pack()

        label_title = ctk.CTkLabel(master=self.reconhecimento_frame, text='Reconhecimento Facial', font=('Arial', 32), text_color='white')
        label_title.pack(pady=(30, 0))

        self.entry_name = ctk.CTkEntry(master=self.reconhecimento_frame, placeholder_text='Digite seu primeiro Nome', width=180)
        self.entry_name.pack(pady=(30, 0))

        label_info = ctk.CTkLabel(master=self.reconhecimento_frame, text='Clique no botão para tirar suas fotos', font=('Arial', 20), text_color='white')
        label_info.pack(pady=(30, 0))

        button_tirar_fotos = ctk.CTkButton(master=self.reconhecimento_frame, text='Tirar Fotos', text_color='white', fg_color='green', hover_color='#014B05', font=('Arial', 20), command=self.tirar_fotos)
        button_tirar_fotos.pack(pady=(30, 0))




    def voltar_do_cadastro(self):
        self.pagina_cadastrar_alunos_frame.pack_forget()
        self.pagina_principal_frame.pack()

    def criar_consultar_alunos(self):
        self.pagina_principal_frame.pack_forget()

        self.pagina_consultar_alunos_frame = ctk.CTkFrame(master=self.janela, width=630, height=650, fg_color='white', corner_radius=0)
        self.pagina_consultar_alunos_frame.pack_propagate(0)
        self.pagina_consultar_alunos_frame.pack(fill='both', expand=True)

        label_title = ctk.CTkLabel(master=self.pagina_consultar_alunos_frame, text='Pagina de Consulta de Alunos', font=('Arial', 32), text_color='black')
        label_title.pack(pady=(50, 0))

        button_voltar = ctk.CTkButton(master=self.pagina_consultar_alunos_frame, width=70, text='Voltar', fg_color='gray', hover_color='#202020', font=('Arial', 20), command=self.voltar_da_consulta)
        button_voltar.pack(pady=(50, 0))
    
    def voltar_da_consulta(self):
        self.pagina_consultar_alunos_frame.pack_forget()
        self.pagina_principal_frame.pack()

    def side_bar(self):
        self.side_bar_pag = ctk.CTkFrame(master=self.janela, width=180, height=680, fg_color='#006CBB')
        self.side_bar_pag.pack_propagate(0)
        self.side_bar_pag.pack(fill='y', anchor='w', side='left')

        button_pag_cadastrar_alunos = ctk.CTkButton(master=self.side_bar_pag, text='Cadastrar Alunos', hover_color='#0159A9', fg_color='transparent', font=('Arial', 20), anchor='w', command=self.criar_cadastrar_alunos)
        button_pag_cadastrar_alunos.pack(anchor='center', ipady=5, pady=(50, 10))

        button_pag_consultar_alunos = ctk.CTkButton(master=self.side_bar_pag, text='Consultar Alunos', hover_color='#0159A9', fg_color='transparent', font=('Arial', 20), anchor='w', command=self.criar_consultar_alunos)
        button_pag_consultar_alunos.pack(anchor='center', ipady=5, pady=(16, 10))

        button_sair_da_conta = ctk.CTkButton(master=self.side_bar_pag, text='Sair da Conta', hover_color='#0159A9', fg_color='transparent', font=('Arial', 20), anchor='w')
        button_sair_da_conta.pack(anchor='center', ipady=5, pady=(420, 10))

    def tirar_fotos(self):
        from Reconhecimento.tirar_fotos import Tirar_Fotos


Application()