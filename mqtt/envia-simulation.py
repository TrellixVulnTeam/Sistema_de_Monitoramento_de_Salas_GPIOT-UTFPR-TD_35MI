# -*- coding: cp1252 -*-
import paho.mqtt.client as mqtt
import random
from time import sleep
from datetime import datetime

client = mqtt.Client()
# conecta no broker
client.connect("127.0.0.1", 1883)
# TOPICOS 
motion = "bloco/E/lab/E-302/SENSOR/MOVIMENTO/"
lamp = "bloco/E/lab/E-302/SENSOR/LAMPADAS/"
windows = "bloco/E/lab/E-302/SENSOR/JANELAS/"



def sensors():
   status = random.choice(["ON ","OFF "])
   iots = random.choice([motion,lamp,windows])
   time = str(datetime.now())[0:-10]
   client.publish(iots,status+time)
   
   print iots,status,time


while True:
    # envia a publicação
    sensors()
    sleep(1)
    
