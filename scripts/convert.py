import os
import subprocess
import re

os.chdir("/home/captcha/")

print(subprocess.check_output(["pwd"]))
list_dir = os.listdir(".")
counter = 0
for dir_name in list_dir:
    os.chdir(dir_name)
    list_file = os.listdir(".")
    for file_name in list_file:
        subprocess.call(["convert", file_name, re.sub('\.gif', '', file_name) + '.jpg'])
        subprocess.call(["rm", file_name])
    os.chdir("..")
    print(counter)
    counter += 1