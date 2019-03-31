import paho.mqtt.client as mqtt
#import RPi.GPIO as GPIO
import json
import pandas as pd
import numpy as np


THINGSBOARD_HOST = 'delrey.td.utfpr.edu.br'
ACCESS_TOKEN = 'EdUPIIVZZSq2gcgr0XRS'

# We assume that all GPIOs are LOW
gpio_state = {7: False, 11: False, 12: False, 13: False, 15: False, 16: False, 18: False, 22: False, 29: False,
              31: False, 32: False, 33: False, 35: False, 36: False, 37: False, 38: False, 40: False}


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
    # Output GPIOs state
 #   GPIO.output(pin, True if status else False)
    # Update GPIOs state
    df = pd.read_csv("data.new.csv")
    STATUS = df['STATUS'].values.tolist()
    PINS = df['PINS'].values.tolist()
    pos = PINS.index(pin)
    change(pos,df,pin,status)
    df.to_csv("data.new.csv",index=False, sep=",")
    print (pin,status) 


    #gpio_state[pin] = status
    #df = pd.read_csv("data.new.csv") # abre 
    #STATUS = df1['STATUS'].values.tolist() # le status de todos os pinos
    #PINS   = df1['PINS'].values.tolist()   # le todos os I/Os
    #pos = PINS.index(pin)    # procura a posicao do pino na lista PINS
    #change(pos,df,pin,status)  # muda no dataframe e salva no csv
    #df.to_csv("data.new.csv",index=False, sep=",")
#    print pin,status


# Using board GPIO layout
# GPIO.setmode(GPIO.BOARD)
# for pin in gpio_state:
    # Set output mode for all GPIO pins
    # GPIO.setup(pin, GPIO.OUT)

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
