#!/usr/bin/env python3

import paho.mqtt.client as mqtt
import time

# MQTT broker details.
mqtt_broker = "localhost"
# mqtt_broker = "127.0.0.1"
# mqtt_broker = "10.0.0.1"

# MQTT communication client.
mqtt_client = mqtt.Client()

def handle_incoming_message(mqtt_client, userdata, msg):
    # Decode the received message.
    decoded_message = str(msg.payload.decode("utf-8"))
    print(decoded_message)
    
    # Logic to process the message (currently commented out).
    if decoded_message[0] != "Client connected" and decoded_message[0] != "Client disconnected":
        print(time.ctime() + ", " +
              decoded_message[0] + " used the RFID card.")
    else:
        print(decoded_message[0] + " : " + decoded_message[1])

def establish_connection():
    # Establish connection with the MQTT broker.
    mqtt_client.connect(mqtt_broker)
    # Set callback function for incoming messages.
    mqtt_client.on_message = handle_incoming_message
    # Subscribe to a topic and start listening.
    mqtt_client.subscribe("worker/card")
    while mqtt_client.loop() == 0:
        pass

def end_connection():
    # Stop the MQTT client loop and disconnect.
    mqtt_client.loop_stop()
    mqtt_client.disconnect()

def initiate_receiver():
    establish_connection()
    # GUI creation logic can be added here.
    # window.mainloop() can be used here if GUI is implemented.
    end_connection()


if __name__ == "__main__":
    initiate_receiver()
