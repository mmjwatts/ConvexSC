#!/usr/bin/env python
import time
import sys
import os
import subprocess
import shutil
import threading

from rgbmatrix import RGBMatrix, RGBMatrixOptions
from PIL import Image, ImageFont, ImageDraw

src_folder = r'/home/pi/update/'

global copy_done
global percentage

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
draw.text((0,29), "  Progress:", (255,255,255),font=font)
matrix.SetImage(image.convert('RGB'))
time.sleep(0.5)

draw.line((4, 94, 4, 100), fill=(255,255,255))
draw.line((59, 94, 59, 100), fill=(255,255,255))
draw.line((4, 94, 59, 94), fill=(255,255,255))
draw.line((4, 100, 59, 100), fill=(255,255,255))

matrix.SetImage(image.convert('RGB'))
time.sleep(0.5)

for x in range(54):
    draw.line((5+x, 95, 5+x, 99), fill=(0,255,0))
    if x > 1:
        draw.line((5+x-1, 95, 5+x-1, 99), fill=(0,200,0))
        if x > 2:
            draw.line((5+x-2, 95, 5+x-2, 99), fill=(0,150,0))
    time.sleep(0.15)
    matrix.SetImage(image.convert('RGB'))
try:
    dest_folder="/home/pi/stockcube_test/"
    if os.path.isdir(dest_folder):
       shutil.rmtree(dest_folder)
#    for f in os.listdir(src_folder):
#        if os.path.isfile(f):
    shutil.copytree(src_folder, dest_folder)

    time.sleep(1)
    draw.rectangle((4, 94, 59, 100), fill=(0,0,0), outline=(0,0,0))
    draw.text((4,93), "Complete", (0,255,0),font=font)
    matrix.SetImage(image.convert('RGB'))
    time.sleep(0.5)

except Exception as e:
    print(e)
    draw.text((4,93), "Error 1", (255,0,0),font=font)
    matrix.SetImage(image.convert('RGB'))
    time.sleep(1)

matrix.SetImage(image.convert('RGB'))
time.sleep(1)

font=ImageFont.load("/home/pi/fonts/7x13B.pil")
draw.text((20,50), "Update", (0,255,0),font=font)
draw.text((2,114), "complete", (0,255,0),font=font)
matrix.SetImage(image.convert('RGB'))
time.sleep(3)
draw.text((20,50), "Update", (0,0,0),font=font)
draw.text((2,114), "complete", (0,0,0),font=font)
matrix.SetImage(image.convert('RGB'))
time.sleep(0.5)
draw.text((0,50), "Rebooting", (0,255,0),font=font)
draw.text((2,114), "now...", (0,255,0),font=font)
matrix.SetImage(image.convert('RGB'))
time.sleep(3)

ps = subprocess.Popen(['sudo', 'reboot'], stdout=subprocess.PIPE)

