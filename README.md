# retroScreen
Software to drive retroScreen

INSTALLATION REQUIREMENTS:

Python and python headers, Raspberry Pi GPIO library, and Adafruit Nokia LCD Library.

```
sudo apt-get install python-pip python-dev build-essential
sudo pip install RPi.GPIO
git clone https://github.com/adafruit/Adafruit_Nokia_LCD
cd Adafruit_Nokia_LCD
sudo python setup.py install
```

Then download this repo:
```
git clone https://github.com/arthurv/retroScreen
```

For GPS, install GPSD and its clients:

```
sudo apt-get install gpsd gpsd-clients python-gps
```
More detailed tutorial in www.aonsquared.co.uk/retroscreen
