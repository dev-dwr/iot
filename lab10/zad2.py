#!/usr/bin/env python3

# pylint: disable=no-member

import time
import RPi.GPIO as GPIO
from config import *  # pylint: disable=unused-wildcard-import
from mfrc522 import MFRC522
from datetime import datetime

running = True

def handleButtonPress(channel):
    global running
    running = False

def alertBuzzer(active):
     GPIO.output(buzzerOutput, not active)  # pylint: disable=no-member

def triggerBuzzer():
    alertBuzzer(True)
    time.sleep(1)
    alertBuzzer(False)

def flashLED():
    GPIO.output(ledIndicator, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(ledIndicator, GPIO.LOW)
    time.sleep(1)

def scanRFID():
    global running
    RFIDReader = MFRC522()
    card_detected = False
    last_detection = datetime.timestamp(datetime.now()) - 3
    while running:
        
        if datetime.timestamp(datetime.now()) - last_detection > 3.0:
            (status, TagType) = RFIDReader.MFRC522_Request(RFIDReader.PICC_REQIDL)
            if status == RFIDReader.MI_OK:
                (status, card_uid) = RFIDReader.MFRC522_Anticoll()
                if status == RFIDReader.MI_OK:
                    scan_time = datetime.now()
                    card_num = 0
                    for i in range(0, len(card_uid)):
                        card_num += card_uid[i] << (i*8)
                    print(f"Card read UID: {card_num}")
                    triggerBuzzer()
                    flashLED()
                    print(f"Date and time of scanning: {scan_time}")
                    last_detection = datetime.timestamp(datetime.now())


def startSystem():
    GPIO.add_event_detect(emergencyButton, GPIO.FALLING, callback=handleButtonPress, bouncetime=200)

    print('Place the card close to the reader (on the right side of the set).')
    scanRFID()


if __name__ == "__main__":
    startSystem()
    GPIO.cleanup()  # pylint: disable=no-member
