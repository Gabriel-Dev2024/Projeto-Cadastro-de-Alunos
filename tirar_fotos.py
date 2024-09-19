import tkinter as tk
import cv2
from PIL import Image, ImageTk
import os

class Tirar_Fotos():
    def __init__(self, janela):
        self.janela = janela
        self.janela.title('Web Cam')

        self.camera = cv2.VideoCapture(0)

        self.current_image = None

        self.canvas = tk.Canvas(janela, width=640, height=480)
        self.canvas.pack()

        self.tirar_foto = tk.Button(janela, text='Tirar Foto', command=self.dowload_images)
        self.tirar_foto.pack(pady=(30, 0))

        self.update_webcam()


    def update_webcam(self):
        while True:
            classific =  cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
            amostra = 1
            num_amostra = 10
            largura = 220
            altura = 220

            conectado, imagem = self.camera.read()
            imagemCinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
            facesdetec = classific.detectMultiScale(imagemCinza, scaleFactor=1.5,minSize=(150,150))

            for (x, y, l, a) in facesdetec:
                cv2.rectangle(imagem, (x,y), (x + l, y + a), (0,0,255))
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    imagemface = cv2.resize(imagemCinza[y:y + a, x:x + l], (largura, altura))
                    cv2.imwrite("fotos/pessoas." + str(id) + "." + str(amostra) + ".jpg", imagemface)
                    print("[foto " + str(amostra) + "capturada com sucesso")
                    amostra += 1

            cv2.imshow("Face", imagem)
            cv2.waitKey(1)
            if amostra >= num_amostra + 1:
                break

        print("Faces capturadas com sucesso!")
        self.camera.release()
        cv2.destroyAllWindows()

    def dowload_images(self):
        if self.current_image is not None:
            file_path = os.path.expanduser('~/Dowloads/Programação/Projeto Cadastro/Fotos/image.png')
            self.current_image.save(file_path)
            os.startfile(file_path)

janela = tk.Tk()

app = Tirar_Fotos(janela)

janela.mainloop()