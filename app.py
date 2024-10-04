import customtkinter as ctk
from customtkinter import *
from tkinter import messagebox, END, filedialog
import bcrypt
from PIL import ImageTk, Image
from PyQt5.QtWidgets import QMessageBox, QApplication
import sys
from DataBase.usuarios_db import DB_Usuarios

class Application(DB_Usuarios):
    def __init__(self):
        self.janela = ctk.CTk()
        self.tema()
        self.tela()
        self.tela_login()
        self.cria_tabela()

        self.selected_images = {
            "certidao_nascimento": None,
            "comprovante_residencia": None,
            "foto_3x4": None,
            "cpf": None,
            "rg": None,
        }
        self.documentos_status = {
            "certidao_nascimento": False,
            "comprovante_residencia": False,
            "foto_3x4": False,
            "cpf": False,
            "rg": False,
        }

        self.janela.mainloop()

    def tema(self):
        # Define o tema da tela
        ctk.set_appearance_mode('light')

    def tela(self):
        # Configurações da tela principal
        self.janela.geometry('700x500')
        self.janela.title('Sistema de Cadastro de Alunos')
        self.janela.resizable(False, False) # Para impedir o usuario de aumentar e diminiur a senha

    # Login
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



    # Cadastro
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
   
       



    # Pagina Principal
    def criar_pagina_principal(self):
        self.login_frame.pack_forget()
        self.janela.geometry('850x650')
        self.side_bar()

        self.pagina_principal_frame = ctk.CTkFrame(master=self.janela, width=700, height=650, fg_color='white', corner_radius=0)
        self.pagina_principal_frame.pack_propagate(0)
        self.pagina_principal_frame.pack(fill='both', expand=True)

        label_pag_principal = ctk.CTkLabel(master=self.pagina_principal_frame, text='Página Principal', font=('Arial', 32), text_color='black')
        label_pag_principal.pack(pady=(50, 0))

        label_mensagem = ctk.CTkLabel(master=self.pagina_principal_frame, text='Bem Vindo ao Sistema de Gerenciamento de Alunos!', font=('Arial', 20), text_color='black')
        label_mensagem.pack(pady=(50, 0))



    # Pagina Cadastrar Alunos
    def criar_cadastrar_alunos(self):
        self.pagina_principal_frame.pack_forget()
        self.side_bar_pag.pack_forget()

        self.pagina_cadastrar_alunos_frame = ctk.CTkFrame(master=self.janela, width=630, height=650, fg_color='white', corner_radius=0)
        self.pagina_cadastrar_alunos_frame.pack_propagate(0)
        self.pagina_cadastrar_alunos_frame.pack(fill='both', expand=True)

        label_title = ctk.CTkLabel(master=self.pagina_cadastrar_alunos_frame, text='Página de Cadastro de Alunos', font=('Arial', 32), text_color='black')
        label_title.pack(pady=(50, 0))

        button_cadastrar = ctk.CTkButton(master=self.pagina_cadastrar_alunos_frame, text='Cadastrar Aluno', hover_color='#0159A9', font=('Arial', 20), anchor='w', command=self.informacoes_pessoais)
        button_cadastrar.pack(pady=(50, 0))

        button_voltar = ctk.CTkButton(master=self.pagina_cadastrar_alunos_frame, width=70, text='Voltar', fg_color='gray', hover_color='#202020', font=('Arial', 20), command=self.voltar_do_cadastro)
        button_voltar.pack(pady=(50, 0))

    def voltar_do_cadastro(self):
        self.pagina_cadastrar_alunos_frame.pack_forget()
        self.criar_pagina_principal()




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

        button_avancar = ctk.CTkButton(master=self.informacoes_pessoais_frame, text='Avançar', fg_color='green', hover_color='#014B05', font=('Arial', 20), command=self.avancar_reconhecimento)
        button_avancar.place(x=280, y=550)

        button_voltar = ctk.CTkButton(master=self.informacoes_pessoais_frame, text='Voltar', fg_color='gray', hover_color='#202020', font=('Arial', 20), command=self.voltar_tela_cadastrar_alunos)
        button_voltar.place(x=130, y=550)

    def avancar_reconhecimento(self):
        if self.validator_informacoes_pessoais():
            self.reconhecimento()

    def voltar_tela_cadastrar_alunos(self):
        self.informacoes_pessoais_frame.pack_forget()
        self.side_bar()
        self.criar_cadastrar_alunos()

    def validator_informacoes_pessoais(self):
        nome_completo_aluno = self.nome_completo_aluno.get().strip()
        data_nascimento = self.data_nascimento.get().strip()
        genero = self.genero.get()
        cpf = self.cpf.get().strip()
        rg = self.rg.get().strip()
        nacionalidade = self.nacionalidade.get().strip()
        naturalidade = self.naturalidade.get().strip()
        estado_civil = self.estado_civil.get()

        if not nome_completo_aluno or not data_nascimento or not genero or not cpf or not rg or not nacionalidade or not naturalidade or not estado_civil:
            messagebox.showerror(title='ERRO', message='Todos as informações pessoais devem ser preenchidos')
            return False
        return True




    def reconhecimento(self):
        self.informacoes_pessoais_frame.pack_forget()
        
        self.reconhecimento_frame = ctk.CTkFrame(master=self.janela, width=550, height=670, fg_color='#006CBB')
        self.reconhecimento_frame.pack_propagate(0)
        self.reconhecimento_frame.pack()

        label_title = ctk.CTkLabel(master=self.reconhecimento_frame, text='Reconhecimento Facial', font=('Arial', 32), text_color='white')
        label_title.pack(pady=(30, 0))

        self.entry_name = ctk.CTkEntry(master=self.reconhecimento_frame, placeholder_text='Digite seu primeiro Nome', width=180)
        self.entry_name.pack(pady=(30, 0))

        self.entry_ano_escolar = ctk.CTkEntry(master=self.reconhecimento_frame, placeholder_text='Digite seu ano Escolar', width=180)
        self.entry_ano_escolar.pack(pady=(20, 0))

        label_info_1 = ctk.CTkLabel(master=self.reconhecimento_frame, text='Clique no botão para tirar suas fotos', font=('Arial', 20), text_color='white')
        label_info_1.pack(pady=(30, 0))

        button_tirar_fotos = ctk.CTkButton(master=self.reconhecimento_frame, text='Tirar Fotos', text_color='white', hover_color='#0159A9', font=('Arial', 20), command=self.tirar_fotos)
        button_tirar_fotos.pack(pady=(20, 0))

        label_info_3 = ctk.CTkLabel(master=self.reconhecimento_frame, text='Após treinar as fotos faça o reconhecimento', font=('Arial', 20), text_color='white')
        label_info_3.pack(pady=(20, 0))

        button_fazer_reconhecimento = ctk.CTkButton(master=self.reconhecimento_frame, text='Fazer Reconhecimento', text_color='white', hover_color='#0159A9', font=('Arial', 20))
        button_fazer_reconhecimento.pack(pady=(20, 0))

        button_avancar = ctk.CTkButton(master=self.reconhecimento_frame, text='Avançar', fg_color='green', hover_color='#014B05', font=('Arial', 20), command=self.avancar_contato)
        button_avancar.place(x=280, y=550)

        button_voltar = ctk.CTkButton(master=self.reconhecimento_frame, text='Voltar', fg_color='gray', hover_color='#202020', font=('Arial', 20), command=self.voltar_informacoes_pessoais)
        button_voltar.place(x=130, y=550)

    def tirar_fotos(self):
        try:
            from Reconhecimento.tirar_fotos import Tirar_Fotos
            self.foto_window = Tirar_Fotos()
            imagem_capturada = self.foto_window.get_foto()  # Chame o novo método

            # Atualizar a imagem no widget
            self.img = ImageTk.PhotoImage(imagem_capturada)
            self.reconhecimento_frame.imgtk = self.img
            self.reconhecimento_frame.configure(image=self.img)

        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro ao tentar tirar fotos: {e}")

    def voltar_informacoes_pessoais(self):
        self.reconhecimento_frame.pack_forget()
        self.informacoes_pessoais_frame.pack()

    def avancar_contato(self):
        if self.validator_reconhecimento():
            self.contato()

    def validator_reconhecimento(self):
        entry_name = self.entry_name.get()
        entry_ano_escolar = self.entry_ano_escolar.get()

        if not entry_name or not entry_ano_escolar:
            messagebox.showerror(title='ERRO', message='Todos os dados devem ser preenchidos')
            return False
        return True




    def contato(self):
        self.reconhecimento_frame.pack_forget()

        self.contato_frame = ctk.CTkFrame(master=self.janela, width=550, height=670, fg_color='#006CBB')
        self.contato_frame.pack_propagate(0)
        self.contato_frame.pack()

        label_title = ctk.CTkLabel(master=self.contato_frame, text='Contato', font=('Arial', 32), text_color='white')
        label_title.pack(pady=(30, 0))

        self.rua_avenida = ctk.CTkEntry(master=self.contato_frame, placeholder_text='Rua/Avenida', font=('Arial', 16), width=300)
        self.rua_avenida.pack(pady=(30, 0))

        self.numero = ctk.CTkEntry(master=self.contato_frame, placeholder_text='Número da Casa', font=('Arial', 16), width=300)
        self.numero.pack(pady=(20, 0))

        self.bairro = ctk.CTkEntry(master=self.contato_frame, placeholder_text='Bairro', font=('Arial', 16), width=300)
        self.bairro.pack(pady=(20, 0))

        self.cidade = ctk.CTkEntry(master=self.contato_frame, placeholder_text='Cidade', font=('Arial', 16), width=300)
        self.cidade.pack(pady=(20, 0))

        self.estado = ctk.CTkEntry(master=self.contato_frame, placeholder_text='Estado', font=('Arial', 16), width=300)
        self.estado.pack(pady=(20, 0))

        self.cep = ctk.CTkEntry(master=self.contato_frame, placeholder_text='CEP', font=('Arial', 16), width=300)
        self.cep.pack(pady=(20, 0))

        self.telefone = ctk.CTkEntry(master=self.contato_frame, placeholder_text='Telefone', font=('Arial', 16), width=350)
        self.telefone.pack(pady=(20, 0))

        self.email = ctk.CTkEntry(master=self.contato_frame, placeholder_text='Email', font=('Arial', 16), width=350)
        self.email.pack(pady=(20, 0))

        button_avancar = ctk.CTkButton(master=self.contato_frame, text='Avançar', fg_color='green', hover_color='#014B05', font=('Arial', 20), command=self.avancar_informacoes_academicas)
        button_avancar.place(x=280, y=550)

        button_voltar = ctk.CTkButton(master=self.contato_frame, text='Voltar', fg_color='gray', hover_color='#202020', font=('Arial', 20), command=self.voltar_reconhecimento)
        button_voltar.place(x=130, y=550)

    def voltar_reconhecimento(self):
        self.contato_frame.pack_forget()
        self.reconhecimento_frame.pack()

    def avancar_informacoes_academicas(self):
        if self.validator_contato():
            self.informacoes_academicas()

    def validator_contato(self):
        rua_avenida = self.rua_avenida.get().strip()
        numero = self.numero.get().strip()
        bairro = self.bairro.get().strip()
        cidade = self.cidade.get().strip()
        estado = self.estado.get().strip()
        cep = self.cep.get().strip()
        telefone = self.telefone.get().strip()
        email = self.email.get().strip()

        if not rua_avenida or not numero or not bairro or not cidade or not estado or not cep or not telefone or not email:
            messagebox.showerror(title='ERRO', message='Todos os dados de contato devem ser preenchidos')
            return False
        return True




    def informacoes_academicas(self):
        self.contato_frame.pack_forget()

        self.informacoes_academicas_frame = ctk.CTkFrame(master=self.janela, width=550, height=670, fg_color='#006CBB')
        self.informacoes_academicas_frame.pack_propagate(0)
        self.informacoes_academicas_frame.pack()

        label_title = ctk.CTkLabel(master=self.informacoes_academicas_frame, text='Informações Acadêmicas', font=('Arial', 32), text_color='white')
        label_title.pack(pady=(30, 0))

        self.numero_matricula = ctk.CTkEntry(master=self.informacoes_academicas_frame, placeholder_text='Número da Matrícula', font=('Arial', 16), width=300)
        self.numero_matricula.pack(pady=(30, 0))

        self.ano_serie = ctk.CTkEntry(master=self.informacoes_academicas_frame, placeholder_text='Ano/Série', font=('Arial', 16), width=300)
        self.ano_serie.pack(pady=(20, 0))

        self.turno = ctk.CTkComboBox(master=self.informacoes_academicas_frame, values=['Matutino', 'Vespertino', 'Noturno'])
        self.turno.pack(anchor='center', pady=(20, 0))

        label_title = ctk.CTkLabel(master=self.informacoes_academicas_frame, text='Clique no botão para fazer o upload do historico escolar', font=('Arial', 20), text_color='white')
        label_title.pack(pady=(30, 0))

        self.historico_escolar = ctk.CTkButton(master=self.informacoes_academicas_frame, text='Upload Histórico', hover_color='#0159A9', font=('Arial',20), command=self.upload_historico)
        self.historico_escolar.pack(pady=(30, 0))

        self.filename_label = ctk.CTkLabel(master=self.informacoes_academicas_frame, text='', font=('Arial', 20), text_color='white')
        self.filename_label.pack(pady=(30, 0))

        button_avancar = ctk.CTkButton(master=self.informacoes_academicas_frame, text='Avançar', fg_color='green', hover_color='#014B05', font=('Arial', 20), command=self.avancar_responsaveis)
        button_avancar.place(x=280, y=550)

        button_voltar = ctk.CTkButton(master=self.informacoes_academicas_frame, text='Voltar', fg_color='gray', hover_color='#202020', font=('Arial', 20), command=self.voltar_contato)
        button_voltar.place(x=130, y=550)

    def voltar_contato(self):
        self.informacoes_academicas_frame.pack_forget()
        self.contato_frame.pack()

    def avancar_responsaveis(self):
        if self.validator_informacoes_academicas():
            self.responsaveis()

    def validator_informacoes_academicas(self):
        numero_matricula = self.numero_matricula.get().strip()
        ano_serie = self.ano_serie.get().strip()
        turno = self.turno.get()

        if not numero_matricula or not ano_serie or not turno:
            messagebox.showerror(title='ERRO', message='Todas as informações acadêmicas devem ser preenchidos')
            return False
        if not hasattr(self, 'nome_historico') or not self.nome_historico:
            messagebox.showerror(title='ERRO', message='Favor fazer o upload do historico escolar')
            return False
        return True
    
    def upload_historico(self):
        global filename
        
        filename = filedialog.askopenfilename(
            initialdir=os.getcwd(),
            title='Selecione o Histórico',
            filetypes=(("Word Document", "*.docx"), ("Text Document", "*.txt"), ("PDF Document", "*.pdf"))
        )

        if filename:
            self.nome_historico = os.path.basename(filename) # Obtém apenas o nome do arquivo
            self.filename_label.configure(text=f'Arquivo Selecionado: {self.nome_historico}')




    def responsaveis(self):
        self.informacoes_academicas_frame.pack_forget()

        self.responsaveis_frame = ctk.CTkFrame(master=self.janela, width=550, height=670, fg_color='#006CBB')
        self.responsaveis_frame.pack_propagate(0)
        self.responsaveis_frame.pack()

        label_title = ctk.CTkLabel(master=self.responsaveis_frame, text='Responsáveis', font=('Arial', 32), text_color='white')
        label_title.pack(pady=(30, 0))

        self.nome_responsavel_1 = ctk.CTkEntry(master=self.responsaveis_frame, placeholder_text='Nome do Reponsável 1', font=('Arial', 16), width=350)
        self.nome_responsavel_1.pack(pady=(30, 0))

        self.grau_parentesco_responsavel_1 = ctk.CTkEntry(master=self.responsaveis_frame, placeholder_text='Grau de Parentesco', font=('Arial', 16), width=300)
        self.grau_parentesco_responsavel_1.pack(pady=(20, 0))

        self.telefone_responsavel_1 = ctk.CTkEntry(master=self.responsaveis_frame, placeholder_text='Telefone', font=('Arial', 16), width=300)
        self.telefone_responsavel_1.pack(pady=(20, 0))

        self.email_responsavel_1 = ctk.CTkEntry(master=self.responsaveis_frame, placeholder_text='Email do Responsável', font=('Arial', 16), width=300)
        self.email_responsavel_1.pack(pady=(20, 0))


        self.nome_responsavel_2 = ctk.CTkEntry(master=self.responsaveis_frame, placeholder_text='Nome do Responsável 2', font=('Arial', 16), width=350)
        self.nome_responsavel_2.pack(pady=(40, 0))

        self.grau_parentesco_responsavel_2 = ctk.CTkEntry(master=self.responsaveis_frame, placeholder_text='Grau de Parentesco', font=('Arial', 16), width=300)
        self.grau_parentesco_responsavel_2.pack(pady=(20, 0))

        self.telefone_responsavel_2 = ctk.CTkEntry(master=self.responsaveis_frame, placeholder_text='Telefone', font=('Arial', 16), width=300)
        self.telefone_responsavel_2.pack(pady=(20, 0))

        self.email_responsavel_2 = ctk.CTkEntry(master=self.responsaveis_frame, placeholder_text='Email do Responsável', font=('Arial', 16), width=300)
        self.email_responsavel_2.pack(pady=(20, 0))

        button_avancar = ctk.CTkButton(master=self.responsaveis_frame, text='Avançar', fg_color='green', hover_color='#014B05', font=('Arial', 20), command=self.avancar_saude_seguranca)
        button_avancar.place(x=280, y=550)

        button_voltar = ctk.CTkButton(master=self.responsaveis_frame, text='Voltar', fg_color='gray', hover_color='#202020', font=('Arial', 20), command=self.voltar_informacoes_academicas)
        button_voltar.place(x=130, y=550)

    def voltar_informacoes_academicas(self):
        self.responsaveis_frame.pack_forget()
        self.informacoes_academicas_frame.pack()

    def avancar_saude_seguranca(self):
        if self.validator_responsaveis():
            self.saude_seguranca()

    def validator_responsaveis(self):
        nome_responsavel_1 = self.nome_responsavel_1.get().strip()
        grau_parentesco_responsavel_1 = self.grau_parentesco_responsavel_1.get().strip()
        telefone_responsavel_1 = self.telefone_responsavel_1.get().strip()
        email_responsavel_1 = self.email_responsavel_1.get().strip()

        nome_responsavel_2 = self.nome_responsavel_2.get().strip()
        grau_parentesco_responsavel_2 = self.grau_parentesco_responsavel_2.get().strip()
        telefone_responsavel_2 = self.telefone_responsavel_2.get().strip()
        email_responsavel_2 = self.email_responsavel_2.get().strip()

        if not nome_responsavel_1 or not grau_parentesco_responsavel_1 or not telefone_responsavel_1 or not email_responsavel_1 or not nome_responsavel_2 or not grau_parentesco_responsavel_2 or not telefone_responsavel_2 or not email_responsavel_2:
            messagebox.showerror(title='ERRO', message='Todos os dados dos responsáveis devem ser preenchidos')
            return False
        return True




    def saude_seguranca(self):
        self.responsaveis_frame.pack_forget()

        self.saude_seguranca_frame = ctk.CTkFrame(master=self.janela, width=550, height=670, fg_color='#006CBB')
        self.saude_seguranca_frame.pack_propagate(0)
        self.saude_seguranca_frame.pack()

        label_title = ctk.CTkLabel(master=self.saude_seguranca_frame, text='Saúde e Segurança', font=('Arial', 32), text_color='white')
        label_title.pack(pady=(30, 0))

        self.plano_saude = ctk.CTkEntry(master=self.saude_seguranca_frame, placeholder_text='Plano de Saúde', font=('Arial', 16), width=350)
        self.plano_saude.pack(pady=(30, 0))

        self.alergias = ctk.CTkEntry(master=self.saude_seguranca_frame, placeholder_text='Alergias do Aluno', font=('Arial', 16), width=350)
        self.alergias.pack(pady=(20, 0))

        self.condicoes_medicas_especiais = ctk.CTkEntry(master=self.saude_seguranca_frame, placeholder_text='Condições Médicas Especiais', font=('Arial', 16), width=350)
        self.condicoes_medicas_especiais.pack(pady=(20, 0))

        contato_emergencia = ctk.CTkLabel(master=self.saude_seguranca_frame, text='Contato de Emergência', font=('Arial', 20), text_color='white')
        contato_emergencia.pack(pady=(30, 0))

        self.nome_emergencia = ctk.CTkEntry(master=self.saude_seguranca_frame, placeholder_text='Nome', font=('Arial', 16), width=300)
        self.nome_emergencia.pack(pady=(20, 0))

        self.telefone_emergencia = ctk.CTkEntry(master=self.saude_seguranca_frame, placeholder_text='Telefone', font=('Arial', 16), width=300)
        self.telefone_emergencia.pack(pady=(20, 0))

        self.relacao_aluno_emergencia = ctk.CTkEntry(master=self.saude_seguranca_frame, placeholder_text='Relação com o Aluno', font=('Arial', 16), width=300)
        self.relacao_aluno_emergencia.pack(pady=(20, 0))

        button_avancar = ctk.CTkButton(master=self.saude_seguranca_frame, text='Avançar', fg_color='green', hover_color='#014B05', font=('Arial', 20), command=self.documentos)
        button_avancar.place(x=280, y=550)

        button_voltar = ctk.CTkButton(master=self.saude_seguranca_frame, text='Voltar', fg_color='gray', hover_color='#202020', font=('Arial', 20), command=self.voltar_responsaveis)
        button_voltar.place(x=130, y=550)

    def voltar_responsaveis(self):
        self.saude_seguranca_frame.pack_forget()
        self.responsaveis_frame.pack()

    def avancar_documentos(self):
        if self.validator_saude_seguranca():
            self.documentos()

    def validator_saude_seguranca(self):
        plano_saude = self.plano_saude.get().strip()
        alergias = self.alergias.get().strip()
        condicoes_medicas_especiais = self.condicoes_medicas_especiais.get().strip()
        nome_emergencia = self.nome_emergencia.get().strip()
        telefone_emergencia = self.telefone_emergencia.get().strip()
        relacao_aluno_emergencia = self.relacao_aluno_emergencia.get().strip()

        if not plano_saude or not alergias or not condicoes_medicas_especiais or not nome_emergencia or not telefone_emergencia or not relacao_aluno_emergencia:
            messagebox.showerror(title='ERRO', message='Todos os dados da saúde e segurança devem ser preenchidos')
            return False
        return True




    def documentos(self):
        self.saude_seguranca_frame.pack_forget()

        self.documentos_frame = ctk.CTkFrame(master=self.janela, width=550, height=670, fg_color='#006CBB')
        self.documentos_frame.pack_propagate(0)
        self.documentos_frame.pack()

        label_title = ctk.CTkLabel(master=self.documentos_frame, text='Documentos', font=('Arial', 32), text_color='white')
        label_title.pack(pady=(30, 0))

        label_informacoes = ctk.CTkLabel(master=self.documentos_frame, text='Faça Upload dos Arquivos', font=('Arial', 20), text_color='white')
        label_informacoes.pack(pady=(30, 0))

        self.certidao_nascimento = ctk.CTkButton(master=self.documentos_frame, text='Certidão de Nascimento', hover_color='#0159A9', font=('Arial',20), command=lambda: self.select_img('certidão_nascimento'))
        self.certidao_nascimento.pack(pady=(30, 0))

        self.comprovante_residencia = ctk.CTkButton(master=self.documentos_frame, text='Comprovante de Residencia', hover_color='#0159A9', font=('Arial', 20), command=lambda: self.select_img('comprovante_residencia'))
        self.comprovante_residencia.pack(pady=(30, 0))

        self.foto_3x4 = ctk.CTkButton(master=self.documentos_frame, text='Foto 3x4', hover_color='#0159A9', font=('Arial', 20), command=lambda: self.select_img('foto_3x4'))
        self.foto_3x4.pack(pady=(30, 0))

        self.cpf = ctk.CTkButton(master=self.documentos_frame, text='CPF do Aluno', hover_color='#0159A9', font=('Arial', 20), command=lambda: self.select_img('cpf'))
        self.cpf.pack(pady=(30, 0))

        self.rg = ctk.CTkButton(master=self.documentos_frame, text='RG do Aluno', hover_color='#0159A9', font=('Arial', 20), command=lambda: self.select_img('rg'))
        self.rg.pack(pady=(30, 0))

        button_avancar = ctk.CTkButton(master=self.documentos_frame, text='Avançar', fg_color='green', hover_color='#014B05', font=('Arial', 20), command=self.informacoes_adicionais) # Colocar a funcao avancar_informacoes_adicionais
        button_avancar.place(x=280, y=550)

        button_voltar = ctk.CTkButton(master=self.documentos_frame, text='Voltar', fg_color='gray', hover_color='#202020', font=('Arial', 20), command=self.voltar_saude_seguranca)
        button_voltar.place(x=130, y=550)

    def voltar_saude_seguranca(self):
        self.documentos_frame.pack_forget()
        self.saude_seguranca_frame.pack()

    def avancar_informacoes_adicionais(self):
        if self.validator_documentos():
            self.informacoes_adicionais()

    def select_img(self, doc_type):
        global filename

        filename = filedialog.askopenfilename(
            initialdir=os.getcwd(),
            title='Selecione as Fotos',
            filetypes=(("JPG Imagem", "*.jpg"), ("JPEG Imagem", "*.jpeg"), ("PNG Imagem", "*.png"))
        )
        if filename:
            self.nome_imagem = os.path.basename(filename)
            self.upload_fotos(filename, doc_type)
            self.documentos_status[doc_type] = True

    def validator_documentos(self):
        # Verifica se todos os documentos foram enviados
        for doc, status in self.documentos_status.items():
            if not status:
                messagebox.showerror(title='ERRO', message=f'Você deve fazer o upload da {doc.replace("_", " ").title()}.')
                return False
        return True




    def informacoes_adicionais(self):
        self.documentos_frame.pack_forget()

        self.informacoes_adicionais_frame = ctk.CTkFrame(master=self.janela, width=550, height=670, fg_color='#006CBB')
        self.informacoes_adicionais_frame.pack_propagate(0)
        self.informacoes_adicionais_frame.pack()

        label_title = ctk.CTkLabel(master=self.informacoes_adicionais_frame, text='Observações Adicionais', font=('Arial', 32), text_color='white')
        label_title.pack(pady=(30, 0))

        label_info = ctk.CTkLabel(master=self.informacoes_adicionais_frame, text='Informações Gerais', font=('Arial', 22), text_color='white')
        label_info.pack(pady=(30, 0))

        self.observacoes_gerais = ctk.CTkTextbox(master=self.informacoes_adicionais_frame, font=('Arial', 16), width=350, height=100)
        self.observacoes_gerais.pack(pady=(20, 0))

        self.necessidades_especiais = ctk.CTkEntry(master=self.informacoes_adicionais_frame, placeholder_text='Necessidades Especiais(Se houver)', font=('Arial', 16), width=350)
        self.necessidades_especiais.pack(pady=(20, 0))

        self.hobbies_interesses = ctk.CTkEntry(master=self.informacoes_adicionais_frame, placeholder_text='Hobbies e Interesses', font=('Arial', 16), width=350)
        self.hobbies_interesses.pack(pady=(20, 0))

        label_info_2 = ctk.CTkLabel(master=self.informacoes_adicionais_frame, text='Autorização para Saídas', font=('Arial', 20), text_color='white')
        label_info_2.pack(pady=(30, 0))

        self.radio_saida = ctk.StringVar(value='')
        self.radio_imagem = ctk.StringVar(value='')

        self.autorizacao_saidas_sim = ctk.CTkRadioButton(master=self.informacoes_adicionais_frame, text='Sim', value='Sim', text_color='white', variable=self.radio_saida)
        self.autorizacao_saidas_sim.place(x=210, y=410)

        self.autorizacao_saidas_nao = ctk.CTkRadioButton(master=self.informacoes_adicionais_frame, text='Não', value='Não', text_color='white', variable=self.radio_saida)
        self.autorizacao_saidas_nao.place(x=290, y=410)

        label_info_3 = ctk.CTkLabel(master=self.informacoes_adicionais_frame, text='Autorização para uso de Imagem', font=('Arial', 20), text_color='white')
        label_info_3.pack(pady=(50, 0))

        self.autorizacao_imagem_sim = ctk.CTkRadioButton(master=self.informacoes_adicionais_frame, text='Sim', value='Sim', text_color='white', variable=self.radio_imagem)
        self.autorizacao_imagem_sim.place(x=210, y=490)

        self.autorizacao_imagem_nao = ctk.CTkRadioButton(master=self.informacoes_adicionais_frame, text='Não', value='Não', text_color='white', variable=self.radio_imagem)
        self.autorizacao_imagem_nao.place(x=290, y=490)

        button_avancar = ctk.CTkButton(master=self.informacoes_adicionais_frame, text='Avançar', fg_color='green', hover_color='#014B05', font=('Arial', 20))
        button_avancar.place(x=280, y=550)

        button_voltar = ctk.CTkButton(master=self.informacoes_adicionais_frame, text='Voltar', fg_color='gray', hover_color='#202020', font=('Arial', 20), command=self.voltar_documentos)
        button_voltar.place(x=130, y=550)

    def voltar_documentos(self):
        self.informacoes_adicionais_frame.pack_forget()
        self.documentos_frame.pack()




    def criar_consultar_alunos(self):
        self.pagina_principal_frame.pack_forget()
        self.side_bar_pag.pack_forget()

        self.pagina_consultar_alunos_frame = ctk.CTkFrame(master=self.janela, width=630, height=650, fg_color='white', corner_radius=0)
        self.pagina_consultar_alunos_frame.pack_propagate(0)
        self.pagina_consultar_alunos_frame.pack(fill='both', expand=True)

        label_title = ctk.CTkLabel(master=self.pagina_consultar_alunos_frame, text='Pagina de Consulta de Alunos', font=('Arial', 32), text_color='black')
        label_title.pack(pady=(50, 0))

        button_voltar = ctk.CTkButton(master=self.pagina_consultar_alunos_frame, width=70, text='Voltar', fg_color='gray', hover_color='#202020', font=('Arial', 20), command=self.voltar_da_consulta)
        button_voltar.pack(pady=(50, 0))
    
    def voltar_da_consulta(self):
        self.pagina_consultar_alunos_frame.pack_forget()
        self.criar_pagina_principal()



    
    def upload_fotos(self, filepath, doc_type):
        global img
        
        img = Image.open(filepath)
        img = img.resize((400, 400))
        img = ImageTk.PhotoImage(img)



        # Armazenar a imagem em formato binário
        with open(filepath, "rb") as file:
            self.selected_images[doc_type] = file.read()

    def side_bar(self):

        # Cria o frame da side bar
        self.side_bar_pag = ctk.CTkFrame(master=self.janela, width=180, height=680, fg_color='#006CBB')
        self.side_bar_pag.pack_propagate(0)
        self.side_bar_pag.pack(fill='y', anchor='w', side='left')

        button_pag_cadastrar_alunos = ctk.CTkButton(master=self.side_bar_pag, text='Cadastrar Alunos', hover_color='#0159A9', fg_color='transparent', font=('Arial', 20), anchor='w', command=self.criar_cadastrar_alunos)
        button_pag_cadastrar_alunos.pack(anchor='center', ipady=5, pady=(50, 10))

        button_pag_consultar_alunos = ctk.CTkButton(master=self.side_bar_pag, text='Consultar Alunos', hover_color='#0159A9', fg_color='transparent', font=('Arial', 20), anchor='w', command=self.criar_consultar_alunos)
        button_pag_consultar_alunos.pack(anchor='center', ipady=5, pady=(16, 10))

        button_sair_da_conta = ctk.CTkButton(master=self.side_bar_pag, text='Sair da Conta', hover_color='#0159A9', fg_color='transparent', font=('Arial', 20), anchor='w', command=self.sair_conta)
        button_sair_da_conta.pack(anchor='center', ipady=5, pady=(420, 10))

    def sair_conta(self):
        self.msg = QMessageBox()
        self.msg.setWindowTitle("Sair da Conta")
        self.msg.setText("Deseja sair da sua conta?")
        res = self.msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

        self.msg.buttonClicked.connect(self.popup_button)

        self.msg.exec_()
    
    def popup_button(self, i):
        if i == self.msg.button(QMessageBox.Yes):
            self.pagina_principal_frame.pack_forget()
            self.side_bar_pag.pack_forget()

            self.tela()
            self.tela_login()
        else:
            return

app = QApplication(sys.argv)
Application()