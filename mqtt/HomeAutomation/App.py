import paho.mqtt.client as mqtt
#import RPi.GPIO as GPIO
import json
import pandas as pd
import numpy as np
import serial
import ast


try:
 arduino = serial.Serial("/dev/ttyACM0",9600)
 print "Arduino Conectado !"
except:
 print ("Porta Nao Encontrada")


THINGSBOARD_HOST = 'delrey.td.utfpr.edu.br'
ACCESS_TOKEN = 'EdUPIIVZZSq2gcgr0XRS'

# We assume that all GPIOs are LOW
gpio_state = {7: False, 11: False, 12: False, 13: False, 15: False, 16: False, 18: False, 22: False, 29: False,
              31: False, 32: False, 33: False, 35: False, 36: False, 37: False, 38: False, 40: False}


data = open("cmds.txt").read()
data = ast.literal_eval(data)


def SendCMDS(data,cmds):
    arduino = serial.Serial("/dev/ttyACM0",9600)
    if cmds[1] == False:
     print ("Desligado !",data[cmds[0]][1])
     command = data[cmds[0]][1]
     arduino.write(command)
    else:
     print ("Ligado !",data[cmds[0]][0])
     command = data[cmds[0]][0]
     arduino.write(command)
#     arduino.write(data[cmds[0]][0])

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, rc, *extra_params):
    print('Connected with result code ' + str(rc))
    # Subscribing to receive RPC requests
    client.subscribe('v1/devices/me/rpc/request/+')
    # Sending current GPIO status
    client.publish('v1/devices/me/attributes', get_gpio_status(), 1)


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print 'Topic: ' + msg.topic + '\nMessage: ' + str(msg.payload)
    # Decode JSON request
    data = json.loads(msg.payload)
    # Check request method
    if data['method'] == 'getGpioStatus':
        # Reply with GPIO status
        client.publish(msg.topic.replace('request', 'response'), get_gpio_status(), 1)
    elif data['method'] == 'setGpioStatus':
        # Update GPIO status and reply
        pin = data['params']['pin']
        status = data['params']['enabled']
        set_gpio_status(pin, status)
        client.publish(msg.topic.replace('request', 'response'), get_gpio_status(), 1)
        client.publish('v1/devices/me/attributes', get_gpio_status(), 1)


def get_gpio_status():
    # Encode GPIOs state to json
    df1 = pd.read_csv("data.new.csv")
    STATUS = df1['STATUS'].values.tolist()
    PINS   = df1['PINS'].values.tolist()
    gpio_state = {}
    for p in range(len(PINS)):
     gpio_state[PINS[p]] = STATUS[p]
    
    #print gpio_state
    return json.dumps(gpio_state)

def change(pos,df,pin,status):
    df[pos:pos+1] = pin,status
    print(pos,pin,status)
    #print ("Saved")

def set_gpio_status(pin, status):
    df = pd.read_csv("data.new.csv")
    STATUS = df['STATUS'].values.tolist()
    PINS = df['PINS'].values.tolist()
    pos = PINS.index(pin)
    change(pos,df,pin,status)
    df.to_csv("data.new.csv",index=False, sep=",")
    cmds = (pin,status)
    SendCMDS(data,cmds) 
    print (pin,status) 



client = mqtt.Client()
# Register connect callback
client.on_connect = on_connect
# Registed publish message callback
client.on_message = on_message
# Set access token
client.username_pw_set(ACCESS_TOKEN)
# Connect to ThingsBoard using default MQTT port and 60 seconds keepalive interval
client.connect(THINGSBOARD_HOST, 1883, 60)

try:
    client.loop_forever()
except KeyboardInterrupt:
    print "Null"
