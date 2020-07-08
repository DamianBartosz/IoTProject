#!/usr/bin/env python3

import paho.mqtt.client as mqtt

import time

import datetime

import RPi.GPIO as GPIO

from GPIOconfig import *  # pylint: disable=unused-wildcard-import
from MQTTconfig import *  # pylint: disable=unused-wildcard-import

import MFRC522
import signal


def on_disconnect():
    print("disconnected")


def publish(cardID):
    client.publish("worker/name", "%d;%d;%s" %
                   (terminalID, cardID, datetime.datetime.now()))

    GPIO.output(led1, GPIO.HIGH)
    time.sleep(0.4)
    GPIO.output(led1, GPIO.LOW)
    GPIO.output(led2, GPIO.HIGH)
    time.sleep(0.4)
    GPIO.output(led2, GPIO.LOW)
    GPIO.output(led3, GPIO.HIGH)
    time.sleep(0.4)
    GPIO.output(led3, GPIO.LOW)
    GPIO.output(led4, GPIO.HIGH)
    time.sleep(0.4)
    GPIO.output(led1, GPIO.HIGH)
    GPIO.output(led2, GPIO.HIGH)
    GPIO.output(led3, GPIO.HIGH)
    time.sleep(0.4)
    GPIO.output(led1, GPIO.LOW)
    GPIO.output(led2, GPIO.LOW)
    GPIO.output(led3, GPIO.LOW)
    GPIO.output(led4, GPIO.LOW)


def rfidRead():
    MIFAREReader = MFRC522.MFRC522()

    while GPIO.input(buttonRed) and GPIO.input(buttonGreen):
        (status, TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
        if status == MIFAREReader.MI_OK:
            (status, uid) = MIFAREReader.MFRC522_Anticoll()
            if status == MIFAREReader.MI_OK:
                num = 0
                for i in range(0, len(uid)):
                    num += uid[i] << (i*8)
                publish(num)


if __name__ == "__main__":
    client.on_disconnect = on_disconnect
    rfidRead()
    GPIO.cleanup()  # pylint: disable=no-member
