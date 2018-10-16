# -*- coding: cp1252 -*-
import paho.mqtt.client as mqtt
import csv 
from time import sleep

 
TOPIC = "home/#"

def csv_writer(data,path):
    with open(path, "wb") as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        for line in data:
             writer.writerow(line)

def pre_processing(topic,payload):
    ambiente = topic.split("/")[1] 
    IoT = topic.split("/")[2] 
    ID = topic.split("/")[3]
    status = 1 if payload.split(" ")[0]=="ON" else 0
    data =  payload.split(" ")[1]
    hora = payload.split(" ")[2]
    dados = [ambiente,IoT,ID,status,data,hora]
    return [["AMBIENTE","DEVICE","ID","STATUS","DATA","HORA"],dados]

def gravar_dado(arquivo,topic,payload):
 with open(arquivo,'a') as log:
        dados = pre_processing(topic,payload)
        writer = csv.writer(log,delimiter=",")
        writer.writerow(dados[1])       
        print "*" * 50 ,"\n\t\tGRAVADO no CSV\n","*" * 50
         
         

 
 
def on_connect(self,client, data, rc):
    self.subscribe([(TOPIC,0)])

 
def on_message(client, userdata, msg):
    print "TOPICO: ",msg.topic,"payload: ",str(msg.payload)
    gravar_dado("home.csv",str(msg.topic),str(msg.payload))
    


# clia um cliente para supervisã0
client = mqtt.Client()

# estabelece as funçõe de conexão e mensagens
client.on_connect = on_connect
client.on_message = on_message

# conecta no broker
client.connect("127.0.0.1", 1883)

# permace em loop, recebendo mensagens
client.loop_forever()