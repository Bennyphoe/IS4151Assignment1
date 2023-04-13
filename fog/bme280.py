from Adafruit_BME280 import *
from gpiozero import MCP3008
from gpiozero import PWMLED
import RPi.GPIO as GPIO
import sqlite3
import math

sensor = BME280(t_mode=BME280_OSAMPLE_8, p_mode=BME280_OSAMPLE_8, h_mode=BME280_OSAMPLE_8)
pot = MCP3008(0)
led = PWMLED(21)
# try:
#     while True:
#         
#         print(sensor.read_temperature())
#         print(pot.value)
#         print(led.value)
#         
# except KeyboardInterrupt:
#     print("Program terminated")
# finally:
#     GPIO.cleanup()

def getTemperatureAndLightLevel():
    temperature = sensor.read_temperature()
    # convert temperature to whole number
    roundedTemperature = str(math.floor(temperature))
    lightLevel = pot.value
    roundedLightLevel = str(round(lightLevel, 3))
    return {"temp": roundedTemperature, "lightLevel": roundedLightLevel}

def toggleLed(toggle):
    if toggle:
        led.value = 1
    else:
        led.value = 0


def flickerLed():
    led.value = 1
    time.sleep(1)
    led.value = 0
    time.sleep(1)