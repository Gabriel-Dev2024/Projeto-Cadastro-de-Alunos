import tkinter as tk
import cv2
from PIL import Image, ImageTk
import os

class Tirar_Fotos():
    def __init__(self, janela):
        self.janela = janela
        self.janela.title('Web Cam')

        self.video_capture = cv2.VideoCapture(0)

        self.current_image = None

        self.canvas = tk.Canvas(janela, width=640, height=480)
        self.canvas.pack()

janela = tk.Tk()

app = Tirar_Fotos(janela)

janela.mainloop()