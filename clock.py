import io
import time

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
		timestr = time.strftime("%H:%M:%S", time.localtime())
		draw.text((0,0), timestr, font=font)
		# Display image.
		disp.image(image)
		disp.display()
	        time.sleep(1)
except KeyboardInterrupt:
	draw.rectangle((0,0,83,47), outline=255, fill=255)
	# Display image.
	disp.image(image)
	disp.display()
