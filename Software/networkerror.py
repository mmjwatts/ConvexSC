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
font2=ImageFont.load("/home/pi/fonts/6x10.pil")

draw.text((0,1), "Network", (255,255,255),font=font)
matrix.SetImage(image.convert('RGB'))
time.sleep(0.1)

draw.text((0,11), "connection", (255,255,255),font=font)
matrix.SetImage(image.convert('RGB'))
time.sleep(0.1)

draw.text((0,21), "error", (255,255,255),font=font)
matrix.SetImage(image.convert('RGB'))
time.sleep(0.1)

time.sleep(1)
draw.text((0,41), "Trying", (255,255,255),font=font)
matrix.SetImage(image.convert('RGB'))
time.sleep(0.1)
draw.text((0,51), "again", (255,255,255),font=font)
matrix.SetImage(image.convert('RGB'))

#Show N/C first and copy debug files before retries as we're in here due to no network in theory
time.sleep(1)
draw.text((2,64), "Wifi", (255,255,255),font=font2)
matrix.SetImage(image.convert('RGB'))
time.sleep(0.5)


#Grab wpa_supplicant and put in log folders. And output of "cat /proc/net/wireless"
ps = subprocess.Popen(['sudo', 'mkdir', '-p', '/home/pi/stockcube/logs/wifi/'], stdout=subprocess.PIPE)
time.sleep(1)

draw.text((44,64), "N/C", (255,125,0),font=font2)
matrix.SetImage(image.convert('RGB'))


ps = subprocess.Popen(['sudo', 'chmod', '-R', 'a+rw', '/home/pi/stockcube/logs/wifi/'], stdout=subprocess.PIPE)
time.sleep(1)

#First "try" doesn't attempt reconnect, but grabs all sorts of logs
tries=1
draw.text((2,118), "Try:", (255,255,255),font=font2)
matrix.SetImage(image.convert('RGB'))
time.sleep(0.5)

ps = subprocess.Popen(['sudo', 'cp', '/etc/wpa_supplicant/wpa_supplicant.conf', '/home/pi/stockcube/logs/wifi/wpa_supplicant.conf'], stdout=subprocess.PIPE)
time.sleep(1)

draw.text((44,118), str(tries), (0,0,255),font=font2)
matrix.SetImage(image.convert('RGB'))

filename='/home/pi/stockcube/logs/wifi/proc_status.txt'
try:
  f = open(filename, "w+")
  ps = subprocess.Popen(['cat', '/proc/net/wireless'], stdout=f)
except:
  try:
    f = open(filename, "w+")
    ps = subprocess.Popen(['cat', '/proc/net/wireless'], stdout=f)
  except:
    print("Failed to open proc_status file")

#Disable Wifi services, and run wpa_supplicant separately to see if it gives more information
ps = subprocess.Popen(['sudo', 'systemctl', 'stop', 'dhcpcd'], stdout=subprocess.PIPE)
print("killing networking...")
time.sleep(3)
ps = subprocess.Popen(['sudo', '/home/pi/stockcube/wpa_supp_debug.sh'], stdout=subprocess.PIPE)
time.sleep(6)
ps = subprocess.Popen(['sudo', 'killall', 'wpa_supplicant'], stdout=subprocess.PIPE)


ps = subprocess.Popen(['sudo', 'systemctl', 'daemon-reload'], stdout=subprocess.PIPE)
ps = subprocess.Popen(['sudo', 'systemctl', 'start', 'dhcpcd'], stdout=subprocess.PIPE)

#Specifically reenable wlan0 in case it's somehow been turned off...
ps = subprocess.Popen(['sudo', 'rfkill', 'unblock', '0'], stdout=subprocess.PIPE)
ps = subprocess.Popen(['sudo', 'ifconfig', 'wlan0', 'up'], stdout=subprocess.PIPE)

while 1:

  tries=tries + 1
  draw.line((0, 118, 64, 118), fill=(0,0,0))
  draw.line((0, 119, 64, 119), fill=(0,0,0))
  draw.line((0, 120, 64, 120), fill=(0,0,0))
  draw.line((0, 121, 64, 121), fill=(0,0,0))
  draw.line((0, 122, 64, 122), fill=(0,0,0))
  draw.line((0, 123, 64, 123), fill=(0,0,0))
  draw.line((0, 124, 64, 124), fill=(0,0,0))
  draw.line((0, 125, 64, 125), fill=(0,0,0))
  draw.line((0, 126, 64, 126), fill=(0,0,0))
  draw.line((0, 127, 64, 127), fill=(0,0,0))

  ps = subprocess.Popen(['cat', '/proc/net/wireless'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
  try:
      output = subprocess.check_output(('grep', 'wlan0'), stdin=ps.stdout)
      #print("Connected to wifi!")
      draw.text((44,64), "N/C", (0,0,0),font=font2)
      matrix.SetImage(image.convert('RGB'))
      draw.text((44,64), "OK", (0,255,0),font=font2)
      time.sleep(1)
      matrix.SetImage(image.convert('RGB'))
      draw.text((0,90), "Connected!", (0,255,0),font=font)
      time.sleep(1)
      matrix.SetImage(image.convert('RGB'))
      draw.text((0,100), "Switch mode", (0,255,0),font=font)
      time.sleep(0.2)
      matrix.SetImage(image.convert('RGB'))
      draw.text((0,110), "to continue", (0,255,0),font=font)
      matrix.SetImage(image.convert('RGB'))
      while 1:
        time.sleep(1)
  except subprocess.CalledProcessError:
      draw.text((2,118), "Try:", (255,255,255),font=font2)
      matrix.SetImage(image.convert('RGB'))
      time.sleep(0.5)
      draw.text((44,118), str(tries), (0,0,255),font=font2)
      matrix.SetImage(image.convert('RGB'))
      ps = subprocess.Popen(['sudo', 'systemctl', 'daemon-reload'], stdout=subprocess.PIPE)
      ps = subprocess.Popen(['sudo', 'systemctl', 'restart', 'dhcpcd'], stdout=subprocess.PIPE)
      time.sleep(4)

