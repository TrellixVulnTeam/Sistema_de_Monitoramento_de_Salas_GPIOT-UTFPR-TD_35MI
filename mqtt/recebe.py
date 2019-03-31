# -*- coding: cp1252 -*-
import paho.mqtt.client as mqtt
from time import sleep
import datetime 
# assinando todas as publicações dentro da area 10
TOPIC = "#"

# função chamada quando a conexão for realizada, sendo
# então realizada a subscrição/

def on_connect(self,client, data, rc):
    self.subscribe([(TOPIC,0)])

# função chamada quando uma nova mensagem do tópico é gerada
def on_message(client, userdata, msg):
    # decodificando o valor recebido
    Payload = str(msg.payload)+" " + str(datetime.datetime.now())
    print "TOPICO: ",msg.topic,"payload: ",str(Payload)
    sleep(0.05)



# clia um cliente para supervisã0
client = mqtt.Client()

# estabelece as funçõe de conexão e mensagens
client.on_connect = on_connect
client.on_message = on_message

# conecta no broker
client.connect("192.168.100.3", 1883)

# permace em loop, recebendo mensagens
client.loop_forever()