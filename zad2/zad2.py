#!/usr/bin/env python3

from config import *
import w1thermsensor
import time
import os
import neopixel
import board
import busio
import adafruit_bme280.advanced as adafruit_bme280

currentParameter = 0
indicatorColor = (255, 0, 0)

temperatureThresholds = [18, 19, 20, 21, 22, 23, 24, 25]
humidityThresholds = [40, 41, 42, 43, 44, 45, 46, 47]
pressureThresholds = [995, 996, 997, 998, 999, 1000, 1001, 1002]

def configureBME280():
    i2c = busio.I2C(board.SCL, board.SDA)
    bme280Sensor = adafruit_bme280.Adafruit_BME280_I2C(i2c, 0x76)
    bme280Sensor.sea_level_pressure = 1013.25
    bme280Sensor.standby_period = adafruit_bme280.STANDBY_TC_500
    bme280Sensor.iir_filter = adafruit_bme280.IIR_FILTER_X16
    return bme280Sensor

def readBME280(bme):
    bme.overscan_pressure = adafruit_bme280.OVERSCAN_X16
    bme.overscan_humidity = adafruit_bme280.OVERSCAN_X1
    bme.overscan_temperature = adafruit_bme280.OVERSCAN_X2
    print(bme.temperature)
    print(bme.humidity)
    print(bme.pressure)
    return {"temperature": bme.temperature, "humidity": bme.humidity, "pressure": bme.pressure}

def configureDiodes(pixel, readings):
    global indicatorColor
    global currentParameter
    pixel.fill((0, 0, 0))
    print(readings["temperature"])
    thresholds = [temperatureThresholds, humidityThresholds, pressureThresholds][currentParameter]
    for i in range(7):
        if thresholds[i] <= readings[list(readings)[currentParameter]] < thresholds[i + 1]:
            pixel[i] = indicatorColor
            break
        pixel[i] = indicatorColor
    pixel.show()

def onButtonPressed(channel):
    global indicatorColor
    global currentParameter
    currentParameter = (currentParameter + 1) % 3
    print("\nButton connected to GPIO " + str(channel) + " pressed.")
    colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
    indicatorColor = colors[currentParameter]

if __name__ == "__main__":
    ledPixels = neopixel.NeoPixel(board.D18, 8, brightness=1.0/32, auto_write=False)
    bme280Sensor = configureBME280()
    GPIO.add_event_detect(buttonRed, GPIO.FALLING, callback=onButtonPressed, bouncetime=200)
    
    while True:
        sensorReadings = readBME280(bme280Sensor)
        configureDiodes(ledPixels, sensorReadings)
