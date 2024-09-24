import cv2
import tkinter as tk
from tkinter import messagebox

class Tirar_Foto:
    def __init__(self, janela):
        self.janela = janela
        self.janela.title("Face Capture")

        self.classific = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
        self.camera = cv2.VideoCapture(0)
        self.amostra = 1
        self.numAmostra = 25
        self.id = input("Digite seu identificador: ")
        self.largura, self.altura = 220, 220

        self.capture_button = tk.Button(janela, text="Capturar Foto", command=self.capture_photo)
        self.capture_button.pack(pady=20)

        self.message_label = tk.Label(janela, text="")
        self.message_label.pack(pady=10)

        self.janela.protocol("WM_DELETE_WINDOW", self.on_closing)

    def capture_photo(self):
        print("Capturando a face...")
        while self.amostra <= self.numAmostra:
            conectado, imagem = self.camera.read()
            imagemCinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
            facesdetec = self.classific.detectMultiScale(imagemCinza, scaleFactor=1.5, minSize=(150, 150))

            for (x, y, l, a) in facesdetec:
                cv2.rectangle(imagem, (x, y), (x + l, y + a), (0, 0, 255))
                imagemface = cv2.resize(imagemCinza[y:y + a, x:x + l], (self.largura, self.altura))
                cv2.imwrite("fotos/pessoas." + str(self.id) + "." + str(self.amostra) + ".jpg", imagemface)
                print(f"[foto {self.amostra} capturada com sucesso")
                self.amostra += 1

            cv2.imshow("Face", imagem)
            cv2.waitKey(1)

            if self.amostra > self.numAmostra:
                break

        messagebox.showinfo("Sucesso", "Faces capturadas com sucesso!")
        self.cleanup()

    def on_closing(self):
        self.cleanup()
        self.janela.destroy()

    def cleanup(self):
        self.camera.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    janela = tk.Tk()
    app = Tirar_Foto(janela)
    janela.mainloop()
