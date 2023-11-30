#!/usr/bin/env python3

# pylint: disable=no-member

import time
import RPi.GPIO as GPIO
from config import *  # pylint: disable=unused-wildcard-import
from mfrc522 import MFRC522
from datetime import datetime
import paho.mqtt.client as mqtt

operation_active = True

device_id = "Device01"
mqtt_broker = "localhost"
mqtt_client = mqtt.Client()


def handleButtonInterrupt(channel):
    global operation_active
    operation_active = False

def setBuzzerState(active):
     GPIO.output(buzzerGPIO, not active)  # pylint: disable=no-member

def activateBuzzer():
    setBuzzerState(True)
    time.sleep(1)
    setBuzzerState(False)

def toggleLED():
    GPIO.output(ledGPIO, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(ledGPIO, GPIO.LOW)
    time.sleep(1)

def readRFID():
    global operation_active
    RFIDReader = MFRC522()
    previous_scan = datetime.timestamp(datetime.now()) - 3
    while operation_active:
        
        if datetime.timestamp(datetime.now()) - previous_scan > 3.0:
            (status, TagType) = RFIDReader.MFRC522_Request(RFIDReader.PICC_REQIDL)
            if status == RFIDReader.MI_OK:
                (status, card_uid) = RFIDReader.MFRC522_Anticoll()
                if status == RFIDReader.MI_OK:
                    current_time = datetime.now()
                    uid_number = 0
                    for i in range(0, len(card_uid)):
                        uid_number += card_uid[i] << (i*8)
                    print(f"Card read UID: {uid_number}")
                    print(f"Date and time of scanning: {current_time}")
                    notifyWorker(uid_number, current_time)
                    activateBuzzer()
                    toggleLED()
                    previous_scan = datetime.timestamp(datetime.now())

def notifyWorker(worker_id, scan_time):
   mqtt_client.publish("worker/card", str(worker_id) + " - " + str(scan_time))

def establishConnection():
   mqtt_client.connect(mqtt_broker)
   notifyWorker("Device Online", datetime.now())

def endConnection():
   notifyWorker("Device Offline", datetime.now())
   mqtt_client.disconnect()

def executeRFIDReader():
    GPIO.add_event_detect(stopButton, GPIO.FALLING, callback=handleButtonInterrupt, bouncetime=200)
    print('Place the card close to the reader.')
    establishConnection()
    readRFID()
    endConnection()

if __name__ == "__main__":
    executeRFIDReader()
    GPIO.cleanup()  # pylint: disable=no-member
