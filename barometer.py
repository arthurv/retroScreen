import io
import time
import psutil
import signal
import sys
import bmp180

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
disp.begin(contrast=50)

# Clear display.
disp.clear()
disp.display()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
image = Image.new('1', (LCD.LCDWIDTH, LCD.LCDHEIGHT))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Load default font.
# Alternatively load a TTF font.
# Some nice fonts to try: http://www.dafont.com/bitmap.php
font = ImageFont.load_default()

def signal_term_handler(signum = None, frame = None):
	sys.stderr.write("Terminated.\n")
	draw.rectangle((0,0,83,47), outline=255, fill=255)
	disp.image(image)
	disp.display()
	sys.exit(0)

for sig in [signal.SIGTERM, signal.SIGINT, signal.SIGHUP, signal.SIGQUIT]: 
	signal.signal(sig, signal_term_handler)

#sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))
try:
	while 1:
		# Clear image buffer.
		draw.rectangle((0,0,83,47), outline=255, fill=255)
		#disp.clear()
		temperature = bmp180.readBmp180()[0]
		pressure = bmp180.readBmp180()[1]
		draw.text((0,0), "temp:", font=font)
		tempstr =  str(temperature) + " C"
		draw.text((0,10), tempstr, font=font)
		draw.text((0,20), "pressure:", font=font)
		presstr = str(pressure) + " mbar"
		draw.text((0,30), presstr, font=font)
		# Display image.
		disp.image(image)
		disp.display()
        	time.sleep(1)
except:
	draw.rectangle((0,0,83,47), outline=255, fill=255)
	# Display image.
	disp.image(image)
	disp.display()
