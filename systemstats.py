import io
import time
import psutil

import Adafruit_Nokia_LCD as LCD
import Adafruit_GPIO.SPI as SPI

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

# Raspberry Pi hardware SPI config:
DC = 23
RST = 24
SPI_PORT = 0
SPI_DEVICE = 0

# Hardware SPI usage:
disp = LCD.PCD8544(DC, RST, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=4000000))

# Software SPI usage (defaults to bit-bang SPI interface):
#disp = LCD.PCD8544(DC, RST, SCLK, DIN, CS)

# Initialize library.
disp.begin(contrast=35)

# Clear display.
disp.clear()
disp.display()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
image = Image.new('1', (LCD.LCDWIDTH, LCD.LCDHEIGHT))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Load default font.
font = ImageFont.load_default()

#sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))
try:
	while 1:
		# Clear image buffer.
		draw.rectangle((0,0,83,47), outline=255, fill=255)
		#disp.clear()
		cpustr = "CPU: " + str(psutil.cpu_percent(interval=None)) + "%"
		draw.text((0,00), cpustr, font=font)
		memstr = "Mem: " + str(psutil.virtual_memory()[2]) + "%"
		draw.text((0,10), memstr, font=font)
		diskstr = "Disk: " + str(psutil.disk_usage("/")[3]) + "%"
		draw.text((0,20), diskstr, font=font)
		#clock
		#timestr = time.strftime("%H:%M:%S", time.localtime())
		tFile = open('/sys/class/thermal/thermal_zone0/temp')
		temp = "Temp: " + "{:.2f}".format(float(tFile.read())/1000) + " C"
		draw.text((0,30), temp, font=font)
		# Display image.
		disp.image(image)
		disp.display()
        	time.sleep(1)
except:
	tFile.close()
	draw.rectangle((0,0,83,47), outline=255, fill=255)
	# Display image.
	disp.image(image)
	disp.display()
