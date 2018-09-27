from Adafruit_IO import Client, Feed, RequestError
from random import choice 
from time import sleep

aio = Client('juanengml', "eb71029ac7904fdeb3878cf0111b6b24")


windows_feed = aio.feeds('Sensor de Janela')
while True:
 windows_data = choice([1,0])
 aio.send(windows_feed.key, windows_data)
 sleep(1)
 print (windows_feed,windows_data)

