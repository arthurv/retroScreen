import io
import time
import psutil
import signal
import sys

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

font = ImageFont.truetype('Volter__28Goldfish_29.ttf', 9)

currline = 0
def lcdprint(printtext=None):
	draw.text((0,9*currline), printtext, font=font)
	currline = (currline+1) % 5


def signal_term_handler(signum = None, frame = None):
	sys.stderr.write("Terminated.\n")
	tFile.close()
	disp.clear()
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
		cpustr = "CPU: " + str(psutil.cpu_percent(interval=None)) + "%"
		lcdprint(cpustr)
		memstr = "Mem: " + str(psutil.virtual_memory()[2]) + "%"
		lcdprint(memstr)
		diskstr = "Disk: " + str(psutil.disk_usage("/")[3]) + "%"
		lcdprint(diskstr)
		tFile = open('/sys/class/thermal/thermal_zone0/temp')
		temp = "Temp: " + "{:.2f}".format(float(tFile.read())/1000) + " C"
		lcdprint(temp)
		# Display image.
		disp.image(image)
		disp.display()
        	time.sleep(1)
except:
	tFile.close()
	# clear display.
	disp.clear()
	disp.display()
