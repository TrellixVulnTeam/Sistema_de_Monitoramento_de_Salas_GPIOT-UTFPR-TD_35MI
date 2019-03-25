import paho.mqtt.client as mqtt
#import RPi.GPIO as GPIO
import json

THINGSBOARD_HOST = 'YOUR_THINGSBOARD_IP_OR_HOSTNAME'
ACCESS_TOKEN = 'RASPBERRY_PI_DEMO_TOKEN'


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, rc, *extra_params):
    print('Connected with result code ' + str(rc))
    # Subscribing to receive RPC requests
    client.subscribe('v1/devices/me/rpc/request/+')
    # Sending current GPIO status
    client.publish('v1/devices/me/attributes', JSON, 1)


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print 'Topic: ' + msg.topic + '\nMessage: ' + str(msg.payload)
    # Decode JSON request
    data = json.loads(msg.payload)
    # Check request method
    if data['method'] == 'getGpioStatus':
        # Reply with GPIO status
        client.publish(msg.topic.replace('request', 'response'), JSON, 1)
    elif data['method'] == 'setGpioStatus':
        # Update GPIO status and reply
        client.publish(msg.topic.replace('request', 'response'), JSON, 1)
        client.publish('v1/devices/me/attributes', JSON, 1)



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
    GPIO.cleanup()
