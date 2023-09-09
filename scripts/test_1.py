from clear_backup import ImageKit, approximation_original, approximation_castom
import re
import os
from PIL import Image

os.chdir("/home/al/session/tsod/ЛР Tesseract/testMulti")
listdir = os.listdir(".")
for capcha_name in listdir:
    path = capcha_name
    obj = ImageKit(path, color_delta=20, height_delta=2,width_delta=1)
    obj.color_define()
    obj.bleach_image()
    obj.pix_4_method()
    obj.pix_7_method()
    obj.rotate_image()

    obj.line_height_method()
    obj.line_width_method()
    obj.pix_7_method()
    #print(obj.weight_pix())
    #obj.image_show()
    #obj.save_image()

    
    if obj.font_test():
        approximation_original(path)
        approximation_original(path)

        obj = ImageKit(path, color_delta=20, height_delta=13,width_delta=7)
        obj.color_define()
        obj.bleach_image()
        obj.pix_7_method()
        obj.rotate_image()
        obj.line_height_method()
        obj.line_width_method()
        obj.pix_7_method()
        #obj.image_show()
        #obj.save_image()
    else:
        obj.save_image()
        name_new_file = approximation_castom("new_" + path)
        img = Image.open(name_new_file)
        #img.show()
    
    print(obj.run_vision("Arial"), "new_Montesuma.ttf_abcfp9.png")
    print(obj.run_vision("eng"), "new_Montesuma.ttf_abcfp9.png")
    print(obj.run_vision("Times"), "new_Montesuma.ttf_abcfp9.png")
    print(obj.run_vision("Minecrafter"), "new_Montesuma.ttf_abcfp9.png")