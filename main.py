
from os import name
import numpy as np
import cv2 as cv
import PIL
from tkinter import ttk
from tkinter import filedialog
from tkinter import *
from PIL import ImageTk, Image
from copy import deepcopy


class MainSolution():
  def __init__(self):
    path = filedialog.askopenfilename(filetypes=(("PNG", "*.png"), ("JPG", "*.jpg"), ("GIF", "*.gif"), ("TIF", "*.tif"), ("BMP", "*.bmp"), ("PCX", "*.pcx")))
    self.image = cv.imread(path)
    self.imgray = cv.cvtColor(self.image, cv.COLOR_BGR2GRAY)
    self.trsh1 = None
    self.trsh2 = None


  def original(self):
    img = Image.fromarray(cv.cvtColor(self.image, cv.COLOR_BGR2RGB))
    img = img.resize((200, 200))
    return ImageTk.PhotoImage(img)

  def global_threshold(self):
    ret, thresh1 = cv.threshold(self.imgray, 0, 255, cv.THRESH_BINARY_INV | cv.THRESH_OTSU)
    self.trsh1 = deepcopy(thresh1)
    img = Image.fromarray(thresh1)
    img = img.resize((200, 200))
    return ImageTk.PhotoImage(img)

  def negative(self):
    negativeimg = cv.cvtColor(self.image, cv.COLOR_BGR2RGB)
    negative = 255 - negativeimg
    img = Image.fromarray(negative)
    img = img.resize((200, 200))
    return ImageTk.PhotoImage(img)

  def global_threshold2(self):
    ret, thresh = cv.threshold(self.imgray, 0, 255, cv.THRESH_BINARY | cv.THRESH_OTSU)
    self.trsh1 = deepcopy(thresh)
    img = Image.fromarray(thresh)
    img = img.resize((200, 200))
    return ImageTk.PhotoImage(img)

  def adaptive_threshold(self):
        thresh2 = cv.adaptiveThreshold(self.imgray, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 11, 2)
        self.trsh2 = deepcopy(thresh2)
        img = Image.fromarray(thresh2)
        img = img.resize((200, 200))
        return ImageTk.PhotoImage(img)

  def multiply(self):
        normalized_image = self.image.astype(np.float32) / 255.0
        multiplied_image = (normalized_image * 1.5 * 255).clip(0, 255).astype(np.uint8)
        img = Image.fromarray(multiplied_image)
        img = img.resize((200, 200))
        return ImageTk.PhotoImage(img)


  def pow2(self):
        normalized_image = self.image.astype(np.float32) / 255.0
        squared_image = (np.power(normalized_image, 2) * 255).clip(0, 255).astype(np.uint8)
        img = Image.fromarray(squared_image)
        img = img.resize((200, 200))
        return ImageTk.PhotoImage(img)

  def linear_contrast(self):
        min_value = np.min(self.image)
        max_value = np.max(self.image)
        new_min = 0
        new_max = 255
        output_image = np.clip(((self.image - min_value) / (max_value - min_value)) * (new_max - new_min) + new_min, 0, 255).astype(np.uint8)
        img = Image.fromarray(output_image)
        img = img.resize((200, 200))
        return ImageTk.PhotoImage(img)

root = Tk()
ms = MainSolution()
w, h = root.winfo_screenwidth(), root.winfo_screenheight()
root.geometry(f"900x600")

methods = [
    ms.original,
    ms.global_threshold,
    ms.global_threshold2,
    ms.adaptive_threshold,
    ms.negative,
    ms.multiply,
    ms.pow2,
    ms.linear_contrast
]

method_labels = [
    "Оригинал",
    "Глобальная пороговая обработка",
    "Глобальная пороговая обработка (2)",
    "Адаптивная пороговая обработка",
    "Негатив",
    "Умножение на константу",
    "Возведение в квадрат",
    "Линейное контрастирование"
]

img_width, img_height = 200, 200
row1, row2 = 4, 8  # Количество методов на верхней и нижней строке

# Верхняя часть окна
for i in range(row1):
    img = methods[i]()
    lbl = ttk.Label(image=img)
    lbl.image = img
    lbl.place(x=i * (img_width + 20) + 30, y=40, width=img_width, height=img_height)
    lbl_text = ttk.Label(text=method_labels[i])
    lbl_text.place(x=i * (img_width + 20) + 30, y=250)

root.mainloop()