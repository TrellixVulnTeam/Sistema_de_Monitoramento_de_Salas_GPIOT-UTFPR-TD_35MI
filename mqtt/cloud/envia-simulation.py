# -*- coding: cp1252 -*-
import paho.mqtt.client as mqtt
import random
from time import sleep
import datetime
import pyautogui

client = mqtt.Client()
# conecta no broker
client.connect("192.168.43.32", 1883)
token = "4iKMYCTSyskXTtP80fpn"
server = "200.134.31.225"
# "bloco/E/lab/302/SENSOR/JANELA/1
# "home/sala/janela/01/status/"
while True:
    menu = pyautogui.confirm(text='Status Janela', title='Simulador MQTT', buttons=['led1-ON', 'led1-OFF','led2-ON','led2-OFF','led3-ON','led3-OFF','led4-ON','led4-OFF'])
    
    client.publish("/makete/",menu)
    if menu=="led1-ON":
        client.publish("/makete/",'q')
    if menu=="led1-OFF":
        client.publish("/makete/",'w')
    if menu=="led2-ON":
        client.publish("/makete/",'e')
    if menu=="led2-OFF":
        client.publish("/makete/",'r')
    if menu=="led3-ON":
        client.publish("/makete/",'t')
    if menu=="led3-OFF":
        client.publish("/makete/",'y')
    if menu=="led4-ON":
        client.publish("/makete/",'u')
    if menu=="led4-OFF":
        client.publish("/makete/",'i')
    if menu=="led5-ON":
        client.publish("/makete/",'o')
    if menu=="led5-OFF":
        client.publish("/makete/",'a')
    if menu=="led6-ON":
        client.publish("/makete/",'d')
    if menu=="led6-OFF":
        client.publish("/makete/",'f')
    if menu=="led7-ON":
        client.publish("/makete/",'g')
    if menu=="led7-OFF":
        client.publish("/makete/",'h')
    if menu=='SAIR': 
        print "EXIT PROGRAMMM"
        break