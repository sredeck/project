#!/usr/local/bin/python3

import RPi.GPIO as GPIO
import time
import sys
import spidev

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
pin_1 = 16
pin_2 = 18

channel = 5
delay = 5

# Open SPI bus
spi = spidev.SpiDev()
spi.open(0,0)

def ReadChannel(channel):
  spi.max_speed_hz = 1000000
  adc = spi.xfer2([1,(8+channel)<<4,0])
  data = ((adc[1]&3) << 8) + adc[2]
  return data

def ConvertPercent(data):
  percent = int(round(data/10.24))
  return percent

def rc_time_1(pin_1):
      count_1 = 0
      #Output on the pin for 
      GPIO.setup(pin_1, GPIO.OUT)
      GPIO.output(16, GPIO.LOW)
      time.sleep(5)
      #Change the pin back to input
      GPIO.setup(pin_1, GPIO.IN)
      #Count until the pin goes high
      while (GPIO.input(pin_1) == GPIO.LOW):
        count_1 += 1
      return count_1

def ConvertPercent_1(count_1):
      percent_1 = int(round(count_1/float(1024)))
      return percent_1


def rc_time_2(pin_2):
      count_2 = 0
      #Output on the pin for 
      GPIO.setup(pin_2, GPIO.OUT)
      GPIO.output(pin_2, GPIO.LOW)
      time.sleep(4)
      #Change the pin back to input
      GPIO.setup(pin_2, GPIO.IN)
      #Count until the pin goes high
      while (GPIO.input(pin_2) == GPIO.LOW):
        count_2 += 1
      return count_2

def ConvertPercent_2(count_2):
      percent_2 = int(round(count_2/float(1024)))
      return percent_2


try:
  # Main loop
   while True:
      moisture_level = ReadChannel(channel)
      moisture_percent = ConvertPercent(moisture_level)
      gas = rc_time_1(pin_1)
      chy = rc_time_2(pin_2)
      if gas is not None:
         print ('----------------------------------')
         print ('CO2:  {} ppm'.format(gas))
      if chy is not None:
         print ('Light:  {} lux'.format(chy))
         print ("Moisture: {} ({}%)".format(moisture_level,moisture_percent))
         time.sleep(delay)

except KeyboardInterrupt:
  pass
finally:
  GPIO.cleanup()
