import os
import sqlite3
from tkinter import filedialog
import customtkinter as ctk
from PIL import Image
from customtkinter import CTkImage
import io

class MyApp:
    def __init__(self, master):
        self.janela = master
        self.selected_images = {
            "certidao_nascimento": None,
            "comprovante_residencia": None,
            "foto_3x4": None,
            "cpf": None,
            "rg": None
        }
        self.documentos()

    def documentos(self):
        self.documentos_frame = ctk.CTkFrame(master=self.janela, width=550, height=670, fg_color='#006CBB')
        self.documentos_frame.pack_propagate(0)
        self.documentos_frame.pack()

        label_title = ctk.CTkLabel(master=self.documentos_frame, text='Documentos', font=('Arial', 32), text_color='white')
        label_title.pack(pady=(30, 0))

        label_informacoes = ctk.CTkLabel(master=self.documentos_frame, text='Faça Upload dos Arquivos', font=('Arial', 20), text_color='white')
        label_informacoes.pack(pady=(30, 0))

        self.certidao_nascimento_btn = ctk.CTkButton(master=self.documentos_frame, text='Certidão de Nascimento', hover_color='#0159A9', font=('Arial', 20), command=lambda: self.select_img('certidao_nascimento'))
        self.certidao_nascimento_btn.pack(pady=(30, 0))

        self.comprovante_residencia_btn = ctk.CTkButton(master=self.documentos_frame, text='Comprovante de Residência', hover_color='#0159A9', font=('Arial', 20), command=lambda: self.select_img('comprovante_residencia'))
        self.comprovante_residencia_btn.pack(pady=(30, 0))

        self.foto_3x4_btn = ctk.CTkButton(master=self.documentos_frame, text='Foto 3x4', hover_color='#0159A9', font=('Arial', 20), command=lambda: self.select_img('foto_3x4'))
        self.foto_3x4_btn.pack(pady=(30, 0))

        self.cpf_btn = ctk.CTkButton(master=self.documentos_frame, text='CPF do Aluno', hover_color='#0159A9', font=('Arial', 20), command=lambda: self.select_img('cpf'))
        self.cpf_btn.pack(pady=(30, 0))

        self.rg_btn = ctk.CTkButton(master=self.documentos_frame, text='RG do Aluno', hover_color='#0159A9', font=('Arial', 20), command=lambda: self.select_img('rg'))
        self.rg_btn.pack(pady=(30, 0))

        button_salvar = ctk.CTkButton(master=self.documentos_frame, text='Salvar Imagens', fg_color='green', hover_color='#014B05', font=('Arial', 20), command=self.save_images_to_db)
        button_salvar.pack(pady=(20, 0))

        button_recarregar = ctk.CTkButton(master=self.documentos_frame, text='Carregar Imagem', fg_color='blue', hover_color='#0055AA', font=('Arial', 20), command=lambda: self.load_image('certidao_nascimento'))
        button_recarregar.pack(pady=(20, 0))

        self.image_label = ctk.CTkLabel(master=self.documentos_frame)
        self.image_label.pack(pady=(20, 0))

    def upload_fotos(self, filepath, document_type):
        img = Image.open(filepath)
        img = img.resize((300, 300))
        img = CTkImage(img)

        self.image_label.configure(image=img)
        self.image_label.Image = img  # Mantenha uma referência da imagem

        # Armazenar a imagem em formato binário
        with open(filepath, "rb") as file:
            self.selected_images[document_type] = file.read()  # Lê a imagem em formato binário

    def select_img(self, document_type):
        filename = filedialog.askopenfilename(
            initialdir=os.getcwd(),
            title='Selecionar Imagem',
            filetypes=(("JPG Imagem", "*.jpg"), ("JPEG Imagem", "*.jpeg"), ("PNG Imagem", "*.png"))
        )
        if filename:
            self.upload_fotos(filename, document_type)

    def save_images_to_db(self):
        conn = sqlite3.connect('meu_banco_de_dados.db')  # Substitua pelo seu banco de dados
        cursor = conn.cursor()

        # Criação de tabela se não existir
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS documentos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tipo TEXT NOT NULL,
                imagem BLOB NOT NULL
            )
        ''')

        for doc_type, image_data in self.selected_images.items():
            if image_data:
                cursor.execute('''
                    INSERT INTO documentos (tipo, imagem) VALUES (?, ?)
                ''', (doc_type, image_data))

        conn.commit()
        conn.close()
        print("Imagens salvas no banco de dados.")

    def load_image(self, document_type):
        conn = sqlite3.connect('meu_banco_de_dados.db')  # Substitua pelo seu banco de dados
        cursor = conn.cursor()

        cursor.execute('SELECT imagem FROM documentos WHERE tipo = ?', (document_type,))
        row = cursor.fetchone()

        if row:
            image_data = row[0]

            # Converte o BLOB de volta para uma imagem
            image = Image.open(io.BytesIO(image_data))
            image = image.resize((300, 300))
            image = CTkImage(image)

            self.image_label.configure(image=image)
            self.image_label.image = image  # Mantenha uma referência da imagem

        conn.close()

if __name__ == '__main__':
    root = ctk.CTk()
    app = MyApp(root)
    root.mainloop()
