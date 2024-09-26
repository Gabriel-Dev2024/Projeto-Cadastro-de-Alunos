import cv2
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os

class Tirar_Fotos:
    def __init__(self):
        self.janela = tk.Tk()
        self.janela.title("Face Capture")
        self.janela.resizable(False, False)

        self.classific = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
        self.camera = cv2.VideoCapture(0)

        if not self.camera.isOpened():
            messagebox.showerror("Erro", "Não foi possível acessar a câmera.")
            self.janela.destroy()
            return

        self.amostra = 1
        self.numAmostra = 25
        self.largura, self.altura = 220, 220
        self.name = 'Gabriel'

        self.capture_button = tk.Button(self.janela, text="Capturar Foto", command=self.capture_photo)
        self.capture_button.pack(pady=5)

        self.message_label = tk.Label(self.janela, text="")
        self.message_label.pack(pady=10)

        self.video_frame = tk.Label(self.janela)
        self.video_frame.pack()

        self.update_frame()  # Inicia a captura de vídeo
        self.janela.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.foto = self.capture_photo()

        self.janela.mainloop()

    def update_frame(self):
        conectado, imagem = self.camera.read()
        if conectado:
            imagemCinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
            facesdetec = self.classific.detectMultiScale(imagemCinza, scaleFactor=1.5, minSize=(150, 150))

            for (x, y, l, a) in facesdetec:
                cv2.rectangle(imagem, (x, y), (x + l, y + a), (0, 0, 255))

            # Converte a imagem para formato que o Tkinter pode usar
            imagem_rgb = cv2.cvtColor(imagem, cv2.COLOR_BGR2RGB)
            self.imagem_pil = Image.fromarray(imagem_rgb)
            self.img = ImageTk.PhotoImage(self.imagem_pil)

            self.video_frame.imgtk = self.img  # Manter a referência
            self.video_frame.configure(image=self.img)


        self.video_frame.after(10, self.update_frame)  # Atualiza o frame a cada 10 ms

    def capture_photo(self):
        if self.amostra <= self.numAmostra:
            conectado, imagem = self.camera.read()
            if not conectado:
                print("Erro ao capturar imagem.")
                return

            imagemCinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
            facesdetec = self.classific.detectMultiScale(imagemCinza, scaleFactor=1.5, minSize=(150, 150))

            for (x, y, l, a) in facesdetec:
                imagemface = cv2.resize(imagemCinza[y:y + a, x:x + l], (self.largura, self.altura))
                
                # Verifica se a pasta 'fotos' existe, caso contrário, cria
                if not os.path.exists('fotos'):
                    os.makedirs('fotos')
                
                cv2.imwrite(f"fotos/pessoas.{self.name}.{self.amostra}.jpg", imagemface)
                print(f"[foto {self.amostra} capturada com sucesso]")
                self.amostra += 1

            if self.amostra > self.numAmostra:
                messagebox.showinfo("Sucesso", "Todas as faces foram capturadas!")
                self.cleanup()

            return self.imagem_pil

    def on_closing(self):
        self.cleanup()
        self.janela.destroy()

    def cleanup(self):
        self.camera.release()
        cv2.destroyAllWindows()

    def get_foto(self):
        return self.foto

Tirar_Fotos()