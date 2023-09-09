from image_box import ImageKit, approximation_original, approximation_castom
import re
import os
from PIL import Image
import subprocess

#font_list = ["Minecraft", "Arial", "Times", "Montesuma", "Ryuk", "Campanella"]
font_list = ["Times"]
for font_name in font_list:
    os.chdir("/home/captcha/" + font_name)

    counter = 0
    list_file = os.listdir(".")
    for file_name in list_file:
        obj = ImageKit(file_name, color_delta=20, height_delta=2,width_delta=1)
        obj.color_define()
        obj.bleach_image()
        obj.pix_4_method()
        obj.pix_7_method()

        obj.line_height_method()
        obj.line_width_method()
        obj.pix_7_method()
        obj.save_image()

        counter += 1
        if counter % 100 == 0:
            print(counter)

font_list = ["Ryuk"]
for font_name in font_list:
    os.chdir("/home/captcha/" + font_name)

    counter = 0
    list_file = os.listdir(".")
    for file_name in list_file:
        obj = ImageKit(file_name, color_delta=20, height_delta=1,width_delta=1)
        obj.color_define()
        obj.bleach_image()
        obj.pix_4_method()
        obj.pix_7_method()

        obj.line_height_method()
        obj.line_width_method()
        obj.pix_7_method()
        obj.save_image()

        counter += 1
        if counter % 100 == 0:
            print(counter)
