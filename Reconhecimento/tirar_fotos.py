import tkinter as tk
import cv2
from PIL import Image, ImageTk
import os

class Tirar_Fotos():
    def __init__(self, janela):
        self.janela = janela
        self.janela.title('Web Cam')

        self.classific = cv2.CascadeClassifier('Reconhecimento/haarcascade_frontalface_default.xml')

        self.camera = cv2.VideoCapture(0)
        self.amostra = 1
        self.num_amostra = 15
        self.largura = 220
        self.altura = 220


        self.current_image = None

        self.canvas = tk.Canvas(janela, width=640, height=480)
        self.canvas.pack()

        self.tirar_foto = tk.Button(janela, text='Tirar Foto', command=self.dowload_images)
        self.tirar_foto.pack()

        self.update_webcam()


    def update_webcam(self):
        ret, imagem = self.camera.read()

        if ret:
            imagem_cinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
            faces_detected = self.classific.detectMultiScale(imagem_cinza, scaleFactor=1.5, minSize=(150, 150))

            for (x, y, l, a) in faces_detected:
                cv2.rectangle(imagem, (x, y), (x + l, y + a), (0, 0, 255))
                imagemface = cv2.resize(imagem_cinza[y:y + a, x:x + l], (self.largura, self.altura))
                




            # self.current_image = ImageTk.PhotoImage(Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))

            self.photo = ImageTk.PhotoImage(image=self.current_image)

            self.canvas.create_image(0, 0, image=self.current_image, anchor=tk.NW)

            self.janela.after(15, self.update_webcam)

    def dowload_images(self):
        if self.current_image is not None:
            file_path = os.path.expanduser('~/Dowloads/Programação/Projeto Cadastro/Fotos/image.png')
            self.current_image.save(file_path)
            os.startfile(file_path)

janela = tk.Tk()

app = Tirar_Fotos(janela)

janela.mainloop()