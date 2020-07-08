#!/usr/bin/env python3

import paho.mqtt.client as mqtt
import socket

# Proszę wpisać hasło do połączenia serwera z brokerem
password = 'db99server'
broker = socket.gethostname()
port = 8883

client = mqtt.Client()


def connect_to_broker():
    client.tls_set("ca.crt")
    client.username_pw_set(username='server', password=password)
    client.connect(broker, port)
