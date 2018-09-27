# Simple example of sending and receiving values from Adafruit IO with the REST
# API client.
# Author: Tony Dicola, Justin Cooper

# Import Adafruit IO REST client.
from Adafruit_IO import Client, Feed,RequestError
import json

# Set to your Adafruit IO key.
# Remember, your key is a secret,
# so make sure not to publish it when you publish this code!
ADAFRUIT_IO_KEY =  "eb71029ac7904fdeb3878cf0111b6b24"

# Set to your Adafruit IO username.
# (go to https://accounts.adafruit.com to find your username)
ADAFRUIT_IO_USERNAME = 'juanengml'

# Create an instance of the REST client.
aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

# List all of your feeds
feeds = aio.feeds()
print(feeds)
try:
    janela = aio.feeds('Janela')
except RequestError:
    feed = Feed(name="Janela")
    janela = aio.create_feed(feed)


