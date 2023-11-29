#!/usr/bin/env python3

from config import *
import RPi.GPIO as GPIO
import time


GPIO.setmode(GPIO.BCM)


led_pwm = GPIO.PWM(led1, 50)
led_pwm.start(0)


encoder_left_previous_state = GPIO.input(encoderLeft)
encoder_right_previous_state = GPIO.input(encoderRight)

brightness_level = 0

def handle_turn_encoder(channel):
    global encoder_left_previous_state
    global encoder_right_previous_state
    global brightness_level

    encoder_left_current_state = GPIO.input(encoderLeft)
    encoder_right_current_state = GPIO.input(encoderRight)


    if encoder_left_previous_state == 1 and encoder_left_current_state == 0 and brightness_level < 100:
        brightness_level += 10
        led_pwm.ChangeDutyCycle(brightness_level)
        print("Brightness:", brightness_level)

    if encoder_right_previous_state == 1 and encoder_right_current_state == 0 and brightness_level > 0:
        brightness_level -= 10
        led_pwm.ChangeDutyCycle(brightness_level)
        print("Brightness:", brightness_level)

    encoder_left_previous_state = encoder_left_current_state
    encoder_right_previous_state = encoder_right_current_state

def main():
    GPIO.setup(encoderLeft, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(encoderRight, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    
    GPIO.add_event_detect(encoderLeft, GPIO.FALLING, callback=handle_turn_encoder, bouncetime=200)
    GPIO.add_event_detect(encoderRight, GPIO.FALLING, callback=handle_turn_encoder, bouncetime=200)

    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        led_pwm.stop()
        GPIO.cleanup()

if __name__ == "__main__":
    main()
