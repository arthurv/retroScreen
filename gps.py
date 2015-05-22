#! /usr/bin/python
# modification of script by Dan Mandle http://dan.mandle.me September 2012
# License: GPL 2.0

# -- BEFORE YOU RUN THIS, SETUP COMMANDS ---
#sudo apt-get install gpsd gpsd-clients python-gps
#sudo dpkg-reconfigure gpsd
#add -n to parameters
#sudo killall gpsd
#sudo gpsd /dev/ttyUSB0 -F /var/run/gpsd.sock
#verify that it is working by using gpsmon (compare with: gpsmon /dev/ttyUSB0)

import io
import psutil
import signal
import sys

import Adafruit_Nokia_LCD as LCD
import Adafruit_GPIO.SPI as SPI

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import os
from gps import *
from time import *
import time
import threading
 
gpsd = None #seting the global variable
 
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

# Load default font.
font = ImageFont.load_default()

def signal_term_handler(signum = None, frame = None):
  sys.stderr.write("Terminated.\n")
  disp.clear()
  disp.display()
  sys.exit(0)

for sig in [signal.SIGTERM, signal.SIGINT, signal.SIGHUP, signal.SIGQUIT]: 
  signal.signal(sig, signal_term_handler)
 
class GpsPoller(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)
    global gpsd #bring it in scope
    gpsd = gps(mode=WATCH_ENABLE) #starting the stream of info
    self.current_value = None
    self.running = True #setting the thread running to true
 
  def run(self):
    global gpsd
    while gpsp.running:
      gpsd.next() #this will continue to loop and grab EACH set of gpsd info to clear the buffer
 
if __name__ == '__main__':
  gpsp = GpsPoller() # create the thread
  try:
    draw.rectangle((0,0,83,47), outline=255, fill=255)
    draw.text((0,10), "No Fix", font=font)
    disp.image(image)
    disp.display()
    gpsp.start() # start it up
    while True:
      #It may take a second or two to get good data
      #print gpsd.fix.latitude,', ',gpsd.fix.longitude,'  Time: ',gpsd.utc
 
      draw.rectangle((0,0,83,47), outline=255, fill=255)
      timestr = time.strftime("%H:%M:%S", time.localtime())
      draw.text((0,0), timestr, font=font)
      latstr = 'lat:' + str(gpsd.fix.latitude)
      draw.text((0,10), latstr, font=font)
      longstr = 'lon:' + str(gpsd.fix.longitude)
      draw.text((0,20), longstr, font=font)
      spdstr = 'spd:' + str(gpsd.fix.speed)
      draw.text((0,30), spdstr, font=font)
      #print 'time utc    ' , gpsd.utc,' + ', gpsd.fix.time
      #print 'altitude (m)' , gpsd.fix.altitude
      #print 'sats        ' , gpsd.satellites
      disp.image(image)
      disp.display()
      time.sleep(5) #set to whatever
 
  except (KeyboardInterrupt, SystemExit): #when you press ctrl+c
    print "\nKilling Thread..."
    gpsp.running = False
    gpsp.join() # wait for the thread to finish what it's doing
  print "Done.\nExiting."