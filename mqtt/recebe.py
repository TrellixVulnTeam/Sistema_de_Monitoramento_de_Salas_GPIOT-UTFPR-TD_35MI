# -*- coding: cp1252 -*-
import paho.mqtt.client as mqtt

from time import sleep

# assinando todas as publicações dentro da area 10
TOPIC = "#"

# função chamada quando a conexão for realizada, sendo
# então realizada a subscrição
def on_connect(self,client, data, rc):
    self.subscribe([(TOPIC,0)])

# função chamada quando uma nova mensagem do tópico é gerada
def on_message(client, userdata, msg):
    # decodificando o valor recebido
    
    #print msg.topic + "/" + str(v)
    
    print "TOPICO: ",msg.topic,"payload: ",str(msg.payload)
    

# clia um cliente para supervisã0
client = mqtt.Client()

# estabelece as funçõe de conexão e mensagens
client.on_connect = on_connect
client.on_message = on_message

# conecta no broker
client.connect("127.0.0.1", 1883)

# permace em loop, recebendo mensagens
client.loop_forever()