import io
import time
import psutil
import signal
import sys
import serial

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

# Initialize library.
disp.begin(contrast=85)
disp.set_contrast(55)

# Clear display.
disp.clear()
disp.display()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
image = Image.new('1', (LCD.LCDWIDTH, LCD.LCDHEIGHT))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

font = ImageFont.truetype('/home/pi/retroScreen/fonts/atomicsc.TTF', 6)

ser = serial.Serial('/dev/ttyAMA0', 9600, timeout=None)

class lcdprinter():
	def __init__(self):
		self.currline = 0
	def println(self,printtext):
		draw.text((1,6*self.currline), printtext, font=font);
		self.currline = (self.currline+1) % 7;

textlcd = lcdprinter()

def signal_term_handler(signum = None, frame = None):
	sys.stderr.write("Terminated.\n")
	ser.close()
	disp.clear()
	disp.display()
	sys.exit(0)

for sig in [signal.SIGTERM, signal.SIGINT, signal.SIGHUP, signal.SIGQUIT]: 
	signal.signal(sig, signal_term_handler)

#sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))
try:
	draw.rectangle((0,0,83,47), outline=255, fill=255)
	textlcd.println("waiting for serial...")
	disp.image(image)
	disp.display()
	while 1:
		# Clear image buffer.
		if textlcd.currline == 0:
			draw.rectangle((0,0,83,47), outline=255, fill=255)
		serial_str = ser.readline()
		if serial_str:
			textlcd.println(serial_str)
		# Display image.
		disp.image(image)
		disp.display()
        	time.sleep(1)
except KeyboardInterrupt:
	ser.close()
	# clear display.
	disp.clear()
	disp.display()
