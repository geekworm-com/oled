# Created by: SupTronics Technologies
# For [X515](https://wiki.geekworm.com/NASPi_CM4-M2) & [X510](https://wiki.geekworm.com/NASPi_CM4-2.5) shield
# Base on Adafruit CircuitPython & SSD1306 Libraries

import time
import board
import busio
# import digitalio

from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306

import subprocess
# import RPi.GPIO as GPIO
# import struct
# import smbus
# import sys

from time import sleep

# Define the Reset Pin
#oled_reset = digitalio.DigitalInOut(board.D4)

# Display Parameters
WIDTH = 128
HEIGHT = 64
BORDER = 5

# Display Refresh
LOOPTIME = 1.0

# Use for I2C.
i2c = board.I2C()
oled = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c, addr=0x3C)

# Clear display.
oled.fill(0)
oled.show()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
image = Image.new("1", (oled.width, oled.height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a white background
draw.rectangle((0, 0, oled.width, oled.height), outline=255, fill=255)

font = ImageFont.truetype('PixelOperator.ttf', 16)
#font = ImageFont.load_default()

# bus = smbus.SMBus(1) # 0 = /dev/i2c-0 (port I2C0), 1 = /dev/i2c-1 (port I2C1)

# PWM fan speed reading
# TACH = 16
# PULSE = 2
# WAIT_TIME = 1

# GPIO.setmode(GPIO.BCM)
# GPIO.setwarnings(False)
# GPIO.setup(TACH, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# t = time.time()
# rpm = 0

# def fell(n):
#     global t
#     global rpm

#     dt = time.time() - t
#     if dt < 0.005: return

#     freq = 1 / dt
#     rpm = (freq / PULSE) * 60
#     t = time.time()

# n = GPIO.add_event_detect(TACH, GPIO.FALLING, fell)

while True:

        #  Draw a black filled box to clear the image.
         draw.rectangle((0, 0, oled.width, oled.height), outline=0, fill=0)

        #  INA219 data reading
        #  Vout = round(ina.voltage(), 3)
        #  Iout = round(ina.current(), 2)
        #  Power = round(ina.power(), 3)
        #  Shunt_V = round(ina.shunt_voltage(), 3)
        #  Load_V  = round((Vout + (Shunt_V/1000)), 3)

        #  Battery data

        #  PWM fan RPM reading
        #  fan = "%.f" % rpm

        # Shell scripts for system monitoring from here : https://unix.stackexchange.com/questions/119126/command-to-display-memory-usage-disk-usage-and-cpu-load
         cmd = "hostname -I | cut -d\' \' -f1"
         IP = subprocess.check_output(cmd, shell = True )
         cmd = "top -bn1 | grep load | awk '{printf \"CPU: %.2f\", $(NF-2)}'"
         CPU = subprocess.check_output(cmd, shell = True )
         cmd = "free -m | awk 'NR==2{printf \"Mem: %s/%sMB %.2f%%\", $3,$2,$3*100/$2 }'"
         MemUsage = subprocess.check_output(cmd, shell = True )
         cmd = "df -h | awk '$NF==\"/\"{printf \"Disk: %d/%dGB %s\", $3,$2,$5}'"
         Disk = subprocess.check_output(cmd, shell = True )
         cmd = "vcgencmd measure_temp |cut -f 2 -d '='"
         Temp = subprocess.check_output(cmd, shell = True )

        #  Pi Stats Display
        #  draw.text((0, 0), "X729 UPS", font=font, fill=255)
        #  draw.text((0, 0), "Vout: " + str(Vout) + " V", font=font, fill=255)
        #  draw.text((0, 16), "Iout: " + str(Iout) + " mA", font=font, fill=255)
        #  draw.text((0, 32), "Power: " + str(Power) + " mW", font=font, fill=255)
        #  draw.text((0, 48), "Shunt_V : " + str(Shunt_V) + " mV", font=font, fill=255)
        #  draw.text((0, 48), "Load_V : " + str(Load_V) + " V", font=font, fill=255)

        #  Battery info
        #  draw.text((0, 48), "BAT:" + str(Vbat) + " V", font=font, fill=255)
        #  draw.text((80, 48), str(Vcap), font=font, fill=255)

         draw.text((0, 0), "IP: " + str(IP,'utf-8'), font=font, fill=255)
         draw.text((0, 16), str(CPU,'utf-8') + "%", font=font, fill=255)
         draw.text((80, 16), str(Temp,'utf-8') , font=font, fill=255)
         draw.text((0, 32), str(MemUsage,'utf-8'), font=font, fill=255)
         draw.text((0, 48), str(Disk,'utf-8'), font=font, fill=255)

        #  draw.text((75, 32), "FAN:" + str(fan), font=font, fill=255)

        #  Display image
         oled.image(image)
         oled.show()
         time.sleep(LOOPTIME)
