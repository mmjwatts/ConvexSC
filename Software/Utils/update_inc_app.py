#!/usr/bin/env python
import time
import sys
import os
import subprocess
import shutil
import threading

from rgbmatrix import RGBMatrix, RGBMatrixOptions
from PIL import Image, ImageFont, ImageDraw

des_mac_app = r'/media/pi/SCSETUP/SCSetup_Mac.app'
src_mac_app = r'/media/pi/SCSETUP/github/Software/Utils/SCSetup_Mac.app'

des_windows_app = r'/media/pi/SCSETUP/WindowsUtils/'
src_windows_app = r'/media/pi/SCSETUP/github/Software/Utils/WindowsUtils/'
des_windows_bat = r'/media/pi/SCSETUP/SCSetup_Win.bat'
src_windows_bat = r'/media/pi/SCSETUP/github/Software/Utils/SCSetup_Win.bat'


global copy_done
global percentage

def checker(source_path, destination_path):

    #Make sure the destination path exists
    while not os.path.exists(destination_path):
        print "doesn't exist"
        time.sleep(0.5)

    #Keep checking the file size until it's the same as source file
    while os.path.getsize(source_path) != os.path.getsize(destination_path):
        percentage = int((float(os.path.get_size(destination_path))/float(os.path.get_size(source_path))) * 100)
        time.sleep(1)
	print(percentage)

    percentage = 100

def copying_file(source_path, destination_path):

    shutil.copytree(source_path, destination_path)
    copy_done = 1

config = {}
with open("/config/cube.txt") as f:
    for line in f:
        name, value = line.split("=")
        config[name] = str(value).rstrip('\n')

#ColourMap = '"' + config["ColourMap"] + '"'
ColourMap = config["ColourMap"]

image_file = "/home/pi/stockcube/blank_screen.png"

image = Image.open(image_file)

draw=ImageDraw.Draw(image)

font=ImageFont.load("/home/pi/fonts/10x20.pil")

draw.text((18,130), "The", (255,255,255),font=font)
draw.text((7,150), "Stock", (255,255,255),font=font)
draw.text((12,170), "Cube", (255,255,255),font=font)

# Configuration for the matrix
options = RGBMatrixOptions()
options.rows = 64
options.cols = 192
options.chain_length = 1
options.brightness = 60
options.parallel = 1
options.pixel_mapper_config = 'Rotate:90'
options.hardware_mapping = 'adafruit-hat'  # If you have an Adafruit HAT: 'adafruit-hat'
options.gpio_slowdown = 1
options.pwm_bits=5
#options.led_rgb_sequence="BGR"
options.led_rgb_sequence=ColourMap
matrix = RGBMatrix(options = options)

# Make image fit our screen.
#image.thumbnail((matrix.width, matrix.height), Image.ANTIALIAS)

matrix.SetImage(image.convert('RGB'))

time.sleep(2)

#draw.text((0,65), "Loading", (255,255,255),font=font)
#matrix.SetImage(image.convert('RGB'))
font=ImageFont.load("/home/pi/fonts/7x13B.pil")

draw.text((4,2), "U", (255,255,255),font=font)
matrix.SetImage(image.convert('RGB'))
time.sleep(0.1)
draw.text((4,2), "Up", (255,255,255),font=font)
matrix.SetImage(image.convert('RGB'))
time.sleep(0.1)
draw.text((4,2), "Upd", (255,255,255),font=font)
matrix.SetImage(image.convert('RGB'))
time.sleep(0.1)
draw.text((4,2), "Upda", (255,255,255),font=font)
matrix.SetImage(image.convert('RGB'))
time.sleep(0.1)
draw.text((4,2), "Updat", (255,255,255),font=font)
matrix.SetImage(image.convert('RGB'))
time.sleep(0.1)
draw.text((4,2), "Updati", (255,255,255),font=font)
matrix.SetImage(image.convert('RGB'))
time.sleep(0.1)
draw.text((4,2), "Updatin", (255,255,255),font=font)
matrix.SetImage(image.convert('RGB'))
time.sleep(0.1)
draw.text((4,2), "Updating", (255,255,255),font=font)
matrix.SetImage(image.convert('RGB'))
time.sleep(0.1)

draw.text((1,66), "s", (255,255,255),font=font)
matrix.SetImage(image.convert('RGB'))
time.sleep(0.1)
draw.text((1,66), "so", (255,255,255),font=font)
matrix.SetImage(image.convert('RGB'))
time.sleep(0.1)
draw.text((1,66), "sof", (255,255,255),font=font)
matrix.SetImage(image.convert('RGB'))
time.sleep(0.1)
draw.text((1,66), "soft", (255,255,255),font=font)
matrix.SetImage(image.convert('RGB'))
time.sleep(0.1)
draw.text((1,66), "softw", (255,255,255),font=font)
matrix.SetImage(image.convert('RGB'))
time.sleep(0.1)
draw.text((1,66), "softwa", (255,255,255),font=font)
matrix.SetImage(image.convert('RGB'))
time.sleep(0.1)
draw.text((1,66), "softwar", (255,255,255),font=font)
matrix.SetImage(image.convert('RGB'))
time.sleep(0.1)
draw.text((1,66), "software", (255,255,255),font=font)
matrix.SetImage(image.convert('RGB'))
time.sleep(0.1)

time.sleep(0.5)

font=ImageFont.load("/home/pi/fonts/6x10_SC.pil")
draw.text((0,19), "Stock cube:", (255,255,255),font=font)
matrix.SetImage(image.convert('RGB'))
time.sleep(0.5)

draw.line((4, 84, 4, 90), fill=(255,255,255))
draw.line((59, 84, 59, 90), fill=(255,255,255))
draw.line((4, 84, 59, 84), fill=(255,255,255))
draw.line((4, 90, 59, 90), fill=(255,255,255))

matrix.SetImage(image.convert('RGB'))
time.sleep(0.5)

for x in range(54):
    draw.line((5+x, 85, 5+x, 89), fill=(0,255,0))
    if x > 1:
        draw.line((5+x-1, 85, 5+x-1, 89), fill=(0,200,0))
        if x > 2:
            draw.line((5+x-2, 85, 5+x-2, 89), fill=(0,150,0))
    time.sleep(0.05)
    matrix.SetImage(image.convert('RGB'))
try:
    src_folder="/media/pi/SCSETUP/github/Software/"
    dest_folder="/home/pi/stockcube/"
    for f in os.listdir(src_folder):
        if os.path.isfile(f):
            shutil.copy(os.path.join(src_folder, f), dest_folder)

    #ps = subprocess.Popen(['sudo', 'mv', '/media/pi/SCSETUP/Software/*', '/home/pi/stockcube/'], stdout=subprocess.PIPE)
    ps = subprocess.Popen(['sudo', 'chmod', '-R', 'a+rwx', '/home/pi/stockcube/'], stdout=subprocess.PIPE)
    if os.path.isfile("/home/pi/stockcube/Version.py"):
        os.remove("/home/pi/stockcube/Version.py")
    shutil.copy("/media/pi/SCSETUP/github/Software/Version.py", "/home/pi/stockcube/")
    time.sleep(1)
    #ps = subprocess.Popen(['sudo', 'mv', '/media/pi/SCSETUP/Setup/Version.py', '/home/pi/stockcube/'], stdout=subprocess.PIPE)
    ps = subprocess.Popen(['sudo', 'chmod', 'a+r', '/home/pi/stockcube/Version.py'], stdout=subprocess.PIPE)

    if os.path.isfile("/media/pi/SCSETUP/GHVersion.py"):
        os.remove("/media/pi/SCSETUP/GHVersion.py")

    time.sleep(1)
    draw.rectangle((4, 84, 59, 90), fill=(0,0,0), outline=(0,0,0))
    draw.text((4,83), "Complete", (0,255,0),font=font)
    matrix.SetImage(image.convert('RGB'))
    time.sleep(0.5)

except Exception as e:
    print(e)
    draw.text((4,83), "Error 1", (255,0,0),font=font)
    matrix.SetImage(image.convert('RGB'))
    time.sleep(1)

draw.text((0,33), "Setup tool:", (255,255,255),font=font)
matrix.SetImage(image.convert('RGB'))
time.sleep(0.5)

draw.line((4, 99, 4, 105), fill=(255,255,255))
draw.line((59, 99, 59, 105), fill=(255,255,255))
draw.line((4, 99, 59, 99), fill=(255,255,255))

draw.line((4, 105, 59, 105), fill=(255,255,255))

matrix.SetImage(image.convert('RGB'))
time.sleep(0.5)

if os.path.exists(src_mac_app):

    print("Removing existing MAC setup app")
    if os.path.exists(des_mac_app):
        shutil.rmtree(des_mac_app)
    print("Removed - starting copy of new one")

    copy_done = 0
    percentage = 0

    t=threading.Thread(name='copying', target=copying_file, args=(src_mac_app, des_mac_app))
    t.start()
    while not os.path.exists(des_mac_app):
        print "doesn't exist"
        time.sleep(0.5)

    while sum([len(files) for r,d,files in os.walk(src_mac_app)]) != sum([len(files) for r,d,files in os.walk(des_mac_app)]):
        for x in range(27):
            draw.line((5+x, 100, 5+x, 104), fill=(0,255,0))
            if x > 1:
                draw.line((5+x-1, 100, 5+x-1, 104), fill=(0,200,0))
                if x > 2:
                    draw.line((5+x-2, 100, 5+x-2, 104), fill=(0,150,0))
            time.sleep(1)
            matrix.SetImage(image.convert('RGB'))

if os.path.exists(src_windows_app):

    print("Removing existing Windows setup app")
    if os.path.exists(des_windows_app):
        shutil.rmtree(des_windows_app)
    print("Removed - starting copy of new one")

    copy_done = 0
    percentage = 0

    t=threading.Thread(name='copying', target=copying_file, args=(src_windows_app, des_windows_app))
    t.start()
    while not os.path.exists(des_windows_app):
        print "doesn't exist"
        time.sleep(0.5)

    while sum([len(files) for r,d,files in os.walk(src_windows_app)]) != sum([len(files) for r,d,files in os.walk(des_windows_app)]):
        for x in range(27):
            draw.line((5+x+27, 100, 5+x+27, 104), fill=(0,255,0))
            if x > 1:
                draw.line((5+x-1+27, 100, 5+x-1+27, 104), fill=(0,200,0))
                if x > 2:
                    draw.line((5+x-2+27, 100, 5+x-2+27, 104), fill=(0,150,0))
            time.sleep(1)
            matrix.SetImage(image.convert('RGB'))

else:
    for x in range(54):
        draw.line((5+x, 100, 5+x, 104), fill=(0,255,0))
        if x > 1:
            draw.line((5+x-1, 100, 5+x-1, 104), fill=(0,200,0))
            if x > 2:
                draw.line((5+x-2, 100, 5+x-2, 104), fill=(0,150,0))
        time.sleep(0.2)
        matrix.SetImage(image.convert('RGB'))

if os.path.isfile(src_windows_bat):
    if os.path.isfile(des_windows_bat):
        os.remove(des_windows_bat)
    shutil.copy(src_windows_bat, des_windows_bat)


#Now copy new version file to Setup folder of USB stick
shutil.copy("/home/pi/stockcube/Version.py", "/media/pi/SCSETUP/Setup/")

draw.rectangle((5, 100, 58, 104), fill=(0,255,0), outline=(0,255,0))
time.sleep(1)
draw.rectangle((4, 99, 59, 105), fill=(0,0,0), outline=(0,0,0))
draw.text((4,98), "Complete", (0,255,0),font=font)
matrix.SetImage(image.convert('RGB'))
time.sleep(1)

shutil.rmtree("/media/pi/SCSETUP/github/")

font=ImageFont.load("/home/pi/fonts/7x13B.pil")
draw.text((20,50), "Update", (0,255,0),font=font)
draw.text((2,114), "complete", (0,255,0),font=font)
matrix.SetImage(image.convert('RGB'))
time.sleep(3)

