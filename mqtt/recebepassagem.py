# -*- coding: cp1252 -*-
import paho.mqtt.client as mqtt
import csv 
from time import sleep
import datetime 
# assinando todas as publicações dentro da area 10
TOPIC = "home/#"

def csv_writer(data,path):
    with open(path, "wb") as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        for line in data:
             writer.writerow(line)

def pre_processing(topic,payload):
    print " +  ",payload
    ambiente = topic.split("/")[1] 
    IoT = topic.split("/")[2] 
    ID = topic.split("/")[3]
    status = payload.split(" ")[0]+" "+payload.split(" ")[1] # USAR AQUI VALOR DE TEM PESSOA OU NAO
    data = payload.split(" ")[2].split(".")[0]  
    hora =  payload.split(" ")[3]
    dados = [ambiente,IoT,ID,status,data,hora]
    print dados
    return [["AMBIENTE","DEVICE","ID","STATUS","DATA","HORA"],dados]

def gravar_dado(arquivo,topic,payload):
 with open(arquivo,'a') as log:
        dados = pre_processing(topic,payload)
        #print dados[0]
        #print dados[1]
        writer = csv.writer(log,delimiter=",")
        writer.writerow(dados[1])       
        print "*" * 20 ,"GRAVADO no CSV","*" * 20
         
         


def on_connect(self,client, data, rc):
    self.subscribe([(TOPIC,0)])

def on_message(client, userdata, msg):
    Payload = str(msg.payload) + str(datetime.datetime.now())
    if "home/sala/porta/" in msg.topic: 	
     print "TOPICO: ",msg.topic
     print "payload:",Payload
     gravar_dado("passagem.csv",str(msg.topic),Payload)
    #if "porta" in msg.topic:
    # print "TOPICO: ",msg.topic,"payload: ",str(Payload),"\n\n"
    sleep(0.05)
 

# clia um cliente para supervisã0
client = mqtt.Client()

# estabelece as funçõe de conexão e mensagens
client.on_connect = on_connect
client.on_message = on_message

# conecta no broker
client.connect("127.0.0.1", 1883)

# permace em loop, recebendo mensagens
client.loop_forever()