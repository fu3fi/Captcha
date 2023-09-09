from collections import Counter
from PIL import Image, ImageFilter, ImageDraw, ImageOps
import numpy as np
import math
import cv2
import matplotlib.pyplot as plt
import random
import pandas as pd
import statsmodels.api as sm
import patsy as pt
import sklearn.linear_model as lm
import os
import time
import re
import subprocess
from typing import Dict

def approximation_original(path):
    subprocess.call(["waifu2x-converter-cpp", "-s", "--disable-gpu", "--scale-ratio", "2", "-i", path, "-o", path])
    return path

def approximation_castom(path):
    subprocess.call(["waifu2x-converter-cpp", "-s", "--disable-gpu", "--scale-ratio", "2", "--noise-level", "3", "-i", re.sub('\.jpg$', '', path) + ".png", "-o", re.sub('\.jpg$', '', path) + ".png"])
    return re.sub('\.jpg$', '', path) + ".png"

class ImageKit():

    def __init__(self, path, color_delta, height_delta=3,width_delta=1):

        # открываем картинку
        self.image = Image.open(path) 

        # задаем имя
        self.image_name = re.sub('.*\/', '', path)

        # определяем ширину
        #self.width = self.image.size[0]

        # определяем высоту
        #self.height = self.image.size[1]

        # выгружаем значения пикселей
        #self.pix = self.image.load()

        # создаем инструмент для рисования
        self.draw = ImageDraw.Draw(self.image) 

        self.color_delta = color_delta
        self.height_delta = height_delta
        self.width_delta = width_delta

    def color_define(self):
        
        # определяем пиксели как массив
        pix_array = np.asarray(self.image)

        # находим отклонение в массиве (вероятно цвет шрифта)
        counter_dict = Counter()
        for value_1 in pix_array.tolist():
            for value_2 in value_1:
                if math.sqrt(value_2[0] ** 2 + value_2[1] ** 2 + value_2[2] ** 2) < 0.8 * math.sqrt(3) * 255:
                    counter_dict[(value_2[0] - value_2[0] % 10, value_2[1] - value_2[1] % 10, value_2[2] - value_2[2] % 10)] += 1

        # сортируем и находим 3 близких
        frequency_list = counter_dict.most_common(3)
        #print(frequency_list)

        # для случая когда цвет текста близок к цвету фона
        if sum(frequency_list[0][0]) > 600:
            lower, upper = [int(x * 0.8) for x in frequency_list[0][0]], [int(x * 1.2) if int(x * 1.2) <= 225 else 225 for x in frequency_list[0][0]]
        else:
            lower, upper = [int(x * 0.8) for x in frequency_list[0][0]], [int(x * 1.2) for x in frequency_list[0][0]]

        self.lower = lower
        self.upper = upper


    def bleach_image(self):
        
        # оставим только цвет шрифта и близких к нему (сделаем черным)
        width = self.image.size[0]
        height = self.image.size[1]
        pix = self.image.load()
        draw = ImageDraw.Draw(self.image) 

        #print(self.lower, self.upper)
        for i in range(width):
            for j in range(height):
                a = pix[i, j][0]
                b = pix[i, j][1]
                c = pix[i, j][2]
                if a >= self.lower[0] - self.color_delta and b >= self.lower[1] - self.color_delta and \
                c >= self.lower[2] - self.color_delta and a <= self.upper[0] + self.color_delta and \
                b <= self.upper[1] + self.color_delta and c <= self.upper[2] + self.color_delta:
                    a, b, c = 0, 0, 0
                else:
                    a, b, c = 255, 255, 255
                draw.point((i, j), (a, b, c))

    def inverted_image(self):
        self.image = ImageOps.invert(self.image)

    def pix_4_method(self):
        width = self.image.size[0]
        height = self.image.size[1]
        pix = self.image.load()
        draw = ImageDraw.Draw(self.image)

        for i in range(width):
            for j in range(height):
                if i == width - 1 or j == height - 1 or i == 0 or j == 0:
                    continue
                if 765 * 3 <= sum(pix[i+1, j]) + sum(pix[i, j+1]) + sum(pix[i-1, j]) + sum(pix[i, j-1]):
                    draw.point((i, j), (255, 255, 255))


    def rotate_image(self):
        self.inverted_image()
        width = self.image.size[0]
        height = self.image.size[1]
        pix = self.image.load()
        new_pixels = list()

        for i in range(width):
            for j in range(height):
                if sum(pix[i, j]) >= 230 * 3: # если цвет не белый (не цвет фона)
                    new_pixels.append((i, height - j))


        random.shuffle(new_pixels)
        clice = int(len(new_pixels)/3)
        data = np.array(new_pixels[:clice])

        # for x, y in data:
        #    plt.scatter(x, y) 
        # plt.show() 

        skm = lm.LinearRegression()
        length = len(data)
        x = np.array([x[0] for x in data]).reshape(length, 1)
        y = np.array([x[1] for x in data]).reshape(length, 1)

        skm.fit(x, y)
        self.image = self.image.rotate(math.degrees(-1 * skm.coef_), resample=Image.BICUBIC, expand=True) # посчитаем коэффициенты
        self.inverted_image()
        self.color_in_black()
        

    def pix_7_method(self):

        width = self.image.size[0]
        height = self.image.size[1]
        pix = self.image.load()
        draw = ImageDraw.Draw(self.image)

        # Заполнение (если у 7 и больше клеток рядом черный цвет - заполняем черным)
        for i in range(width):
            for j in range(height):
                if i == width - 1 or j == height - 1 or i == 0 or j == 0:
                    continue
                if 765 * 3 >= sum(pix[i+1, j]) + sum(pix[i+1, j+1]) + sum(pix[i, j+1]) + sum(pix[i-1, j+1]) + sum(pix[i-1, j]) + sum(pix[i-1, j-1]) + sum(pix[i, j-1]) + sum(pix[i+1, j-1]): 
                    draw.point((i, j), (0, 0, 0))

    
    def color_in_black(self):

        width = self.image.size[0]
        height = self.image.size[1]
        pix = self.image.load()
        draw = ImageDraw.Draw(self.image)

        # cделаем изображение без рамытия (только черный и белый пиксель)
        for i in range(width):
            for j in range(height):
                if sum(pix[i, j]) < 600:
                    draw.point((i, j), (0, 0, 0))
                else:
                    draw.point((i, j), (255, 255, 255))


 

    def line_height_method(self):

        width = self.image.size[0]
        height = self.image.size[1]
        pix = self.image.load()
        draw = ImageDraw.Draw(self.image)

        # очистка методом вертикальных линий
        draw = ImageDraw.Draw(self.image)
        height_sum = 0
        for i in range(width):
            for j in range(height):
                height_sum += sum(pix[i, j])
            if height_sum > (height - self.height_delta) * 255 * 3:
                for j in range(height):
                    draw.point((i, j), (255, 255, 255))
            height_sum = 0

    def line_width_method(self):

        width = self.image.size[0]
        height = self.image.size[1]
        pix = self.image.load()
        draw = ImageDraw.Draw(self.image)

        # очистка методом горизонтальных линий
        draw = ImageDraw.Draw(self.image)
        width_sum = 0
        for j in range(height):
            for i in range(width):
                width_sum += sum(pix[i, j])
            if width_sum > (width - self.width_delta) * 255 * 3:
                for i in range(width):
                    draw.point((i, j), (255, 255, 255))
            width_sum = 0


    def image_show(self):
        self.image.show()


    def save_image(self):
        self.image.save(re.sub("\.jpg$", "", self.image_name) + ".png", "png")

    def font_test(self):
        width = self.image.size[0]
        height = self.image.size[1]
        pix = self.image.load()

        pix_black_sum = 0
        for i in range(width):
            for j in range(height):
                if sum(pix[i, j]) == 0:
                    pix_black_sum += 1

        #return pix_black_sum / (width * height)
        if pix_black_sum / (width * height) < 0.01:
            return True
        return False

    def weight_pix(self):
        width = self.image.size[0]
        height = self.image.size[1]
        pix = self.image.load()

        pix_black_sum = 0
        for i in range(width):
            for j in range(height):
                if sum(pix[i, j]) == 0:
                    pix_black_sum += 1

        with open("weight_pix.txt", 'a') as open_file:
            open_file.write(str(pix_black_sum / (width * height)) + '\n')
        return pix_black_sum / (width * height)

    def run_vision(self, lang):
        new_name = "new_" + re.sub("\.jpg$", "", self.image_name) + ".png"
        subprocess.call(["tesseract", "-l", lang, new_name, "out_" + re.sub('\.png', '', new_name)])
        print("out_" + re.sub('\.png', '', new_name) + ".txt")
        return {
            "lang": lang,
            "result": subprocess.check_output(["cat", "out_" + re.sub('\.png', '', new_name) + ".txt"]).decode("utf-8"),
        }

    '''
    def start(name):
        subprocess.call(["waifu2x-converter-cpp", "-s", "--disable-gpu", "--scale-ratio", "2", "-i", name, "-o", name])
        new_name = post_effect_line(test_capcha(name))
        subprocess.call(["tesseract", "-l", "eng", new_name, "out_" + re.sub('\.png', '', new_name)])
        return re.sub('[^0-9a-z]', '', subprocess.check_output(["cat", "out_" + re.sub('\.png', '', new_name) + ".txt"]).decode("utf-8"))



    os.chdir("/home/al/session/tsod/ЛР Tesseract/Campanella")
    listdir = os.listdir(".")

    cycle_all = 0
    lucky = 0


    #start("/home/al/session/tsod/ЛР Tesseract/green_6/Minecraft.ttf_chptw3.jpg")
    for capcha_name in listdir:
        cod = start(capcha_name)
        print(cod)
        if cod == re.sub('\.jpg$', '', re.sub('[A-Za-z]*\.ttf\_', '', capcha_name)).strip():
            lucky += 1
            cycle_all += 1
        else:
            cycle_all += 1
            
        print(lucky/cycle_all)
    '''