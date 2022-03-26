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

time.sleep(1)

#draw.text((0,65), "Loading", (255,255,255),font=font)
#matrix.SetImage(image.convert('RGB'))

try:
  sys.path.append("/home/pi/stockcube/")
  import Version
  font=ImageFont.load("/home/pi/fonts/5x7.pil")
  draw.text((0,122), "v"+str(Version.Version), (255,255,255),font=font)
  matrix.SetImage(image.convert('RGB'))
except:
  matrix.SetImage(image.convert('RGB'))

time.sleep(1)

font=ImageFont.load("/home/pi/fonts/9x18B.pil")

y_coord = 65
draw.text((0,y_coord), "L", (255,255,255),font=font)
matrix.SetImage(image.convert('RGB'))
time.sleep(0.1)
draw.text((0,y_coord), "Lo", (255,255,255),font=font)
matrix.SetImage(image.convert('RGB'))
time.sleep(0.1)
draw.text((0,y_coord), "Loa", (255,255,255),font=font)
matrix.SetImage(image.convert('RGB'))
time.sleep(0.1)
draw.text((0,y_coord), "Load", (255,255,255),font=font)
matrix.SetImage(image.convert('RGB'))
time.sleep(0.1)
draw.text((0,y_coord), "Loadi", (255,255,255),font=font)
matrix.SetImage(image.convert('RGB'))
time.sleep(0.1)
draw.text((0,y_coord), "Loadin", (255,255,255),font=font)
matrix.SetImage(image.convert('RGB'))
time.sleep(0.1)
draw.text((0,y_coord), "Loading", (255,255,255),font=font)
matrix.SetImage(image.convert('RGB'))
time.sleep(0.1)

y_coord=y_coord+15
draw.text((13,y_coord), "y", (255,255,255),font=font)
matrix.SetImage(image.convert('RGB'))
time.sleep(0.1)
draw.text((13,y_coord), "yo", (255,255,255),font=font)
matrix.SetImage(image.convert('RGB'))
time.sleep(0.1)
draw.text((13,y_coord), "you", (255,255,255),font=font)
matrix.SetImage(image.convert('RGB'))
time.sleep(0.1)
draw.text((13,y_coord), "your", (255,255,255),font=font)
matrix.SetImage(image.convert('RGB'))
time.sleep(0.1)

y_coord = y_coord+15
draw.text((9,y_coord), "s", (255,255,255),font=font)
matrix.SetImage(image.convert('RGB'))
time.sleep(0.1)
draw.text((9,y_coord), "se", (255,255,255),font=font)
matrix.SetImage(image.convert('RGB'))
time.sleep(0.1)
draw.text((9,y_coord), "set", (255,255,255),font=font)
matrix.SetImage(image.convert('RGB'))
time.sleep(0.1)
draw.text((9,y_coord), "setu", (255,255,255),font=font)
matrix.SetImage(image.convert('RGB'))
time.sleep(0.1)
draw.text((9,y_coord), "setup", (255,255,255),font=font)
matrix.SetImage(image.convert('RGB'))
time.sleep(0.1)

y_coord=y_coord+10
time.sleep(0.5)
draw.text((18,y_coord), ".", (255,255,255),font=font)
matrix.SetImage(image.convert('RGB'))
time.sleep(0.5)
draw.text((28,y_coord), ".", (255,255,255),font=font)
matrix.SetImage(image.convert('RGB'))
time.sleep(0.5)
draw.text((38,y_coord), ".", (255,255,255),font=font)
matrix.SetImage(image.convert('RGB'))

time.sleep(0.5)
draw.text((18,y_coord), ".", (0,0,0),font=font)
draw.text((28,y_coord), ".", (0,0,0),font=font)
draw.text((38,y_coord), ".", (0,0,0),font=font)
matrix.SetImage(image.convert('RGB'))

time.sleep(0.5)
draw.text((18,y_coord), ".", (255,255,255),font=font)
matrix.SetImage(image.convert('RGB'))
time.sleep(0.5)
draw.text((28,y_coord), ".", (255,255,255),font=font)
matrix.SetImage(image.convert('RGB'))
time.sleep(0.5)
draw.text((38,y_coord), ".", (255,255,255),font=font)
matrix.SetImage(image.convert('RGB'))

time.sleep(0.5)

draw.text((18,y_coord), ".", (0,0,0),font=font)
draw.text((28,y_coord), ".", (0,0,0),font=font)
draw.text((38,y_coord), ".", (0,0,0),font=font)
matrix.SetImage(image.convert('RGB'))

time.sleep(0.5)

#font=ImageFont.load("/home/pi/fonts/5x7.pil")
#font=ImageFont.load("/home/pi/fonts/6x9_MWa.pil")
font=ImageFont.load("/home/pi/fonts/6x10.pil")
#font=ImageFont.load("/home/pi/fonts/7x13B.pil")

draw.text((2,0), "Wifi", (255,255,255),font=font)
matrix.SetImage(image.convert('RGB'))

#x = 1
#if x == 1:
try:
    with open("/home/pi/Setup/wifi.txt", "r") as wififile:
        for line in wififile:
            currentline = line.split(";")
            wifi_SSID=str(currentline[0])
            wifi_PWD=str(currentline[1])
	    try:
	      wifi_country=str((currentline[2].split(":"))[0])
	      wifi_key_mgmt=str(currentline[3])
	      wifi_timezone=str(currentline[4])
            except: #Allows for case where old format setup file is present (shouldn't happen...!)
	      wifi_country="US"
	      wifi_key_mgmt="WPA-PSK"
	      wifi_timezone="Europe/London"

    file = open("/home/pi/stockcube/wpa_supplicant.conf_new", "w")
    file.write("ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev\n")
    file.write("update_config=1\n")
    file.write("country=" + wifi_country + "\n")
    file.write("\n")
    file.write("network={\n")
    file.write("    ssid=\"" + wifi_SSID + "\"\n")
    file.write("    psk=\"" + wifi_PWD + "\"\n")
    file.write("    key_mgmt=" + wifi_key_mgmt + "\n")
    file.write("}\n")
    file.close()
    file = open("/config/timezone.h", "w")
    file.write("char local_tz[30] = \"" + wifi_timezone + "\";\n")
    file.close()
    ps = subprocess.Popen(['sudo', 'mv', '/etc/wpa_supplicant/wpa_supplicant.conf', '/etc/wpa_supplicant/wpa_supplicant.conf_old'], stdout=subprocess.PIPE)
    ps = subprocess.Popen(['sudo', 'mv', '/home/pi/stockcube/wpa_supplicant.conf_new', '/etc/wpa_supplicant/wpa_supplicant.conf'], stdout=subprocess.PIPE)

    ps = subprocess.Popen(['sudo', 'systemctl', 'daemon-reload'], stdout=subprocess.PIPE)
    ps = subprocess.Popen(['sudo', 'systemctl', 'restart', 'dhcpcd'], stdout=subprocess.PIPE)

    time.sleep(4)
    ps = subprocess.Popen(['cat', '/proc/net/wireless'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    try:
        output = subprocess.check_output(('grep', 'wlan0'), stdin=ps.stdout)
        print("Connected to wifi!")
        draw.text((50,0), "OK", (0,255,0),font=font)
        matrix.SetImage(image.convert('RGB'))
    except subprocess.CalledProcessError:
        draw.text((32,0), "Try 1", (0,0,255),font=font)
        matrix.SetImage(image.convert('RGB'))
        time.sleep(4)
        ps = subprocess.Popen(['cat', '/proc/net/wireless'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        draw.text((32,0), "Try 1", (0,0,0),font=font) #Clear text ready for next update
        try:
            output = subprocess.check_output(('grep', 'wlan0'), stdin=ps.stdout)
            print("Connected to wifi!")
            draw.text((50,0), "OK", (0,255,0),font=font)
            matrix.SetImage(image.convert('RGB'))
        except subprocess.CalledProcessError:
            draw.text((32,0), "Try 2", (0,0,255),font=font)
            matrix.SetImage(image.convert('RGB'))
            time.sleep(4)
            ps = subprocess.Popen(['cat', '/proc/net/wireless'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            draw.text((32,0), "Try 2", (0,0,0),font=font) #Clear text ready for next update
            try:
                output = subprocess.check_output(('grep', 'wlan0'), stdin=ps.stdout)
                print("Connected to wifi!")
                draw.text((50,0), "OK", (0,255,0),font=font)
                matrix.SetImage(image.convert('RGB'))
            except subprocess.CalledProcessError:
                draw.text((32,0), "Try 3", (0,0,255),font=font)
                matrix.SetImage(image.convert('RGB'))
                time.sleep(4)
                draw.text((32,0), "Try 3", (0,0,0),font=font) #Clear text ready for next update
                ps = subprocess.Popen(['cat', '/proc/net/wireless'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                try:
                    output = subprocess.check_output(('grep', 'wlan0'), stdin=ps.stdout)
                    print("Connected to wifi!")
                    draw.text((50,0), "OK", (0,255,0),font=font)
                    matrix.SetImage(image.convert('RGB'))
                except subprocess.CalledProcessError:
                    draw.text((44,0), "N/C", (255,125,0),font=font)
                    matrix.SetImage(image.convert('RGB'))

except Exception as e:
    print(e)
    draw.text((50,0), "E1", (255,0,0),font=font)
    matrix.SetImage(image.convert('RGB'))

time.sleep(2)

draw.text((2,12), "API Key", (255,255,255),font=font)
matrix.SetImage(image.convert('RGB'))

time.sleep(2)

draw.text((50,12), "OK", (0,255,0),font=font)
matrix.SetImage(image.convert('RGB'))

time.sleep(1)

draw.text((2,24), "Tickers", (255,255,255),font=font)
matrix.SetImage(image.convert('RGB'))

time.sleep(2)

draw.text((50,24), "OK", (0,255,0),font=font)
matrix.SetImage(image.convert('RGB'))

time.sleep(1)

draw.text((2,36), "Mode 1", (255,255,255),font=font)
matrix.SetImage(image.convert('RGB'))

time.sleep(2)

#Remove existing check_prices file (called every minute by crontab)
if os.path.isfile("/home/pi/check_prices.py"):
    os.remove("/home/pi/check_prices.py")

try:
    sys.path.append("/home/pi/Setup")
    import mode1
    modefile="/home/pi/stockcube/mode" + str(mode1.modeFront) + str(mode1.modeTop)
    if os.path.isfile("/home/pi/stockcube/SC_mode1"):
        os.remove("/home/pi/stockcube/SC_mode1")
    shutil.copy(modefile, "/home/pi/stockcube/SC_mode1")

    draw.text((50,36), "OK", (0,255,0),font=font)
    matrix.SetImage(image.convert('RGB'))
    mode1OK=1
except:
    draw.text((50,36), "E1", (255,0,0),font=font)
    matrix.SetImage(image.convert('RGB'))
    mode1OK=0

time.sleep(1)

draw.text((2,48), "Mode 2", (255,255,255),font=font)
matrix.SetImage(image.convert('RGB'))

time.sleep(2)

try:
    sys.path.append("/home/pi/Setup")
    import mode2
    modefile="/home/pi/stockcube/mode" + str(mode2.modeFront) + str(mode2.modeTop)
    if os.path.isfile("/home/pi/stockcube/SC_mode2"):
        os.remove("/home/pi/stockcube/SC_mode2")
    shutil.copy(modefile, "/home/pi/stockcube/SC_mode2")

    draw.text((50,48), "OK", (0,255,0),font=font)
    matrix.SetImage(image.convert('RGB'))
    mode2OK=1
except:
    draw.text((50,48), "E1", (255,0,0),font=font)
    matrix.SetImage(image.convert('RGB'))
    mode2OK=0

#Now write the check_prices.py file dependent on modes
file = open("/home/pi/check_prices.sh", "w")
file.write("#/bin/bash\n")
file.write("/home/pi/stockcube/check_network_time.sh 1\n")
file.write("nw_status=$?\n")
file.write("echo $nw_status > /home/pi/nw_status.txt\n")
file.write("if [ $nw_status -eq 0 ]\n")
file.write("then\n")
#Only run price checks if we have network connection!
if mode1OK == 1 and mode2OK == 1:
  if mode1.modeFront == 0 or mode2.modeFront == 0: #Watchlist mode
    file.write("python /home/pi/stockcube/check_watchlist.py\n")
  if mode1.modeFront == 1 or mode2.modeFront == 1 or mode1.modeTop == 1 or mode2.modeTop == 1: #Portfolio mode
    file.write("python /home/pi/stockcube/check_portfolio.py\n")
  if mode1.modeTop == 0 or mode2.modeTop == 0: #ETF mode
    file.write("python /home/pi/stockcube/check_etfs.py\n")
  if mode1.modeTop == 2 or mode2.modeTop == 2: #Exchange mode
    file.write("python /home/pi/stockcube/check_exchanges.py\n")
else:
    file.write("python /home/pi/stockcube/check_etfs.py\n")
    #If there were any issues with user modes,
    #setup default mode20 file so stuff doesn't break (doesn't require any user setups)
    modefile="/home/pi/stockcube/mode20"
    if os.path.isfile("/home/pi/stockcube/SC_mode1"):
        os.remove("/home/pi/stockcube/SC_mode1")
    shutil.copy(modefile, "/home/pi/stockcube/SC_mode1")
    if os.path.isfile("/home/pi/stockcube/SC_mode2"):
        os.remove("/home/pi/stockcube/SC_mode2")
    shutil.copy(modefile, "/home/pi/stockcube/SC_mode2")

file.write("/home/pi/stockcube/nyse_status\n")
file.write("fi\n")
file.close()
ps = subprocess.Popen(['sudo', 'chmod', '-R', 'a+x', '/home/pi/check_prices.sh'], stdout=subprocess.PIPE)

time.sleep(2)

font=ImageFont.load("/home/pi/fonts/9x18B.pil")
y_coord=65
draw.text((0,y_coord), "Loading", (0,0,0),font=font)
draw.text((13,y_coord+15), "your", (0,0,0),font=font)
draw.text((9,y_coord+15+15), "setup", (0,0,0),font=font)
matrix.SetImage(image.convert('RGB'))
time.sleep(0.5)

#Unmount USB stick safely - done in startup.sh
#ps = subprocess.Popen(['sudo', 'umount', '-f', '/media/pi/SCSETUP'], stdout=subprocess.PIPE)

font=ImageFont.load("/home/pi/fonts/6x10.pil")
draw.text((15,65), "Setup", (255,255,255),font=font)
draw.text((5,75), "complete!", (255,255,255),font=font)
matrix.SetImage(image.convert('RGB'))
time.sleep(1)

draw.text((15,91), "Please", (0,0,255),font=font)
draw.text((15,101), "remove", (0,0,255),font=font)
draw.text((4,111), "USB stick", (0,0,255),font=font)
matrix.SetImage(image.convert('RGB'))
time.sleep(1)

usb_removed=0
while usb_removed < 1:
    ps = subprocess.Popen(['sudo', 'tail', '-n', '5', '/var/log/messages'], stdout=subprocess.PIPE)
    try:
        output = subprocess.check_output(('grep', 'USB disconnect'), stdin=ps.stdout)
        print("USB removed!")
        usb_removed=1
    except:
        usb_removed=0
    time.sleep(2)

draw.text((15,91), "Please", (0,0,0),font=font)
draw.text((15,101), "remove", (0,0,0),font=font)
draw.text((4,111), "USB stick", (0,0,0),font=font)
matrix.SetImage(image.convert('RGB'))

draw.text((5,101), "Let's go!", (0,255,0),font=font)
matrix.SetImage(image.convert('RGB'))
time.sleep(4)
