#!/usr/bin/env python3

from config import *
import w1thermsensor
import time
import os
import neopixel
import board
import busio
import adafruit_bme280.advanced as adafruit_bme280
from PIL import Image, ImageDraw, ImageFont
import lib.oled.SSD1331 as OLED_Display

def initialize_sensor():
    i2c_connection = busio.I2C(board.SCL, board.SDA)
    climate_sensor = adafruit_bme280.Adafruit_BME280_I2C(i2c_connection, 0x76)
    climate_sensor.sea_level_pressure = 1013.25
    climate_sensor.standby_period = adafruit_bme280.STANDBY_TC_500
    climate_sensor.iir_filter = adafruit_bme280.IIR_FILTER_X16
    return climate_sensor

def read_climate_data(sensor):
    sensor.overscan_pressure = adafruit_bme280.OVERSCAN_X16
    sensor.overscan_humidity = adafruit_bme280.OVERSCAN_X1
    sensor.overscan_temperature = adafruit_bme280.OVERSCAN_X2
    print(sensor.temperature)
    print(sensor.humidity)
    print(sensor.pressure)
    return {"temp" : round(sensor.temperature, 2), "hum" : round(sensor.humidity, 2), "press" : round(sensor.pressure, 2)}

def update_display(data):
    oled = OLED_Display.SSD1331()
    oled.Init()
    image_screen = Image.new("RGB", (oled.width, oled.height), "WHITE")
    draw_screen = ImageDraw.Draw(image_screen)
    large_font = ImageFont.truetype('./lib/oled/Font.ttf', 20)
    small_font = ImageFont.truetype('./lib/oled/Font.ttf', 8)

    img_temp = Image.open('./pictures/temperature.jpg')
    img_temp = img_temp.resize((15, 10))
    img_hum = Image.open('./pictures/humidity.png')
    img_hum = img_hum.resize((15, 10))
    img_press = Image.open('./pictures/pressure.png')
    img_press = img_press.resize((15, 10))

    image_screen.paste(img_temp, (0, 0))
    draw_screen.text((17,0), f'Temp: {data["temp"]}', font=small_font, fill="BLACK")

    image_screen.paste(img_hum, (0, 25))
    draw_screen.text((17,25), f'Humidity: {data["hum"]}', font=small_font, fill="BLACK")

    image_screen.paste(img_press, (0, 50))
    draw_screen.text((17,50), f'Pressure: {data["press"]}', font=small_font, fill="BLACK")
    
    oled.ShowImage(image_screen, 0, 0)


if __name__ == "__main__":
    led_strip = neopixel.NeoPixel(board.D18, 8, brightness=1.0/32, auto_write=False)
    climate_sensor = initialize_sensor()
    
    while True:
        sensor_data = read_climate_data(climate_sensor)
        update_display(sensor_data)
    oled.clear()
