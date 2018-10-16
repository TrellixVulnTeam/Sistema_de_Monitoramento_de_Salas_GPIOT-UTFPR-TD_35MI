# -*- coding: cp1252 -*-
import paho.mqtt.client as mqtt
import random
from time import sleep
import datetime
import pyautogui

client = mqtt.Client()
# conecta no broker
client.connect("127.0.0.1", 1883)


while True:
    menu = pyautogui.confirm(text='Status Janela', title='Simulador MQTT', buttons=['ON', 'OFF','SAIR'])
    if menu=='ON': client.publish("home/sala/janela/01/status/","ON "+str(datetime.datetime.now()))
    if menu=='OFF': client.publish("home/sala/janela/01/status/","OFF "+str(datetime.datetime.now()))
    if menu=='SAIR': 
        print "EXIT PROGRAMMM"
        break

    
    
