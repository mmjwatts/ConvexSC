#!/usr/bin/env python
import time
import sys
import os
import subprocess
import shutil

from rgbmatrix import RGBMatrix, RGBMatrixOptions
from PIL import Image, ImageFont, ImageDraw

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
options.pwm_bits=6
#options.led_rgb_sequence="BGR"
options.led_rgb_sequence=ColourMap
matrix = RGBMatrix(options = options)

# Make image fit our screen.
#image.thumbnail((matrix.width, matrix.height), Image.ANTIALIAS)

matrix.SetImage(image.convert('RGB'))

time.sleep(2)

#draw.text((0,65), "Loading", (255,255,255),font=font)
#matrix.SetImage(image.convert('RGB'))
#font=ImageFont.load("/home/pi/fonts/9x18B.pil")
#font=ImageFont.load("/home/pi/fonts/7x13B.pil")
font=ImageFont.load("/home/pi/fonts/6x9_MWa.pil")
font2=ImageFont.load("/home/pi/fonts/5x7.pil")

draw.text((0,1), "Cube time", (255,255,255),font=font)
matrix.SetImage(image.convert('RGB'))
time.sleep(0.1)

draw.text((0,10), "not synced", (255,255,255),font=font)
matrix.SetImage(image.convert('RGB'))
time.sleep(0.1)

time.sleep(2)

draw.text((0,25), "This just", (255,255,255),font=font2)
matrix.SetImage(image.convert('RGB'))
time.sleep(0.1)
draw.text((0,35), "takes a few", (255,255,255),font=font2)
matrix.SetImage(image.convert('RGB'))
time.sleep(0.1)

draw.text((0,45), "ticks after", (255,255,255),font=font2)
matrix.SetImage(image.convert('RGB'))
time.sleep(0.1)

draw.text((0,55), "first boot", (255,255,255),font=font2)
matrix.SetImage(image.convert('RGB'))
time.sleep(0.1)

time.sleep(3)

draw.text((0,65), "Cube will", (255,255,255),font=font2)
matrix.SetImage(image.convert('RGB'))
time.sleep(0.1)
draw.text((0,75), "run \"offline", (255,255,255),font=font2)
matrix.SetImage(image.convert('RGB'))
time.sleep(0.1)
draw.text((0,85), "mode\" until", (255,255,255),font=font2)
matrix.SetImage(image.convert('RGB'))
time.sleep(0.1)
draw.text((0,95), "sync happens", (255,255,255),font=font2)
matrix.SetImage(image.convert('RGB'))
time.sleep(0.1)
draw.text((0,105), "automatically", (255,255,255),font=font2)
matrix.SetImage(image.convert('RGB'))

#font=ImageFont.load("/home/pi/fonts/5x7.pil")
#font=ImageFont.load("/home/pi/fonts/6x10.pil")

time.sleep(6)
