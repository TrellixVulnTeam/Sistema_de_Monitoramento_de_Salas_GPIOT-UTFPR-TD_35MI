# -*- coding: cp1252 -*-
import paho.mqtt.client as mqtt
import csv 
from time import sleep
import datetime
 
TOPIC = "home/#"

def csv_writer(data,path):
    with open(path, "wb") as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        for line in data:
             writer.writerow(line)

def pre_processing(topic,payload,opcao):
    if opcao==0:
        ambiente = topic.split("/")[1] 
        IoT = topic.split("/")[2] 
        ID = topic.split("/")[3]
        status = payload.split()[0]
        data =  payload.split()[1]
        hora = payload.split()[2].split(".")[0]
        dados = [ambiente,IoT,ID,status,data,hora]
        print 0,dados
        return [["AMBIENTE","DEVICE","ID","STATUS","DATA","HORA"],dados]
    if opcao==1:
        ambiente = topic.split("/")[1] 
        IoT = topic.split("/")[2] 
        ID = topic.split("/")[3]
        status = payload.split(" ")[0]+" "+payload.split(" ")[1]+" "+payload.split(" ")[2]
        data = payload.split(" ")[3].split(".")[0]  
        hora =  payload.split(" ")[4]
        dados = [ambiente,IoT,ID,status,data,hora]
        print 1,dados
        return [["AMBIENTE","DEVICE","ID","STATUS","DATA","HORA"],dados]



def gravar_dado(arquivo,topic,payload,opcao):
 with open(arquivo,'a') as log:
        dados = pre_processing(topic,payload,opcao)
        writer = csv.writer(log,delimiter=",")
        writer.writerow(dados[1])       
        print dados
        print "*" * 50 ,"\n\t\tGRAVADO no CSV\n","*" * 50
         
         

 
 
def on_connect(self,client, data, rc):
    self.subscribe([(TOPIC,0)])

 
def on_message(client, userdata, msg):
<<<<<<< HEAD
    sleep(2)
    if ("/sala/janela/01/status/" in msg.topic):
=======
    if "/sala/janela/03/status/" in msg.topic:
>>>>>>> eb23d16fd79c82247943502c318d00d4766771fb
     Payload = str(msg.payload) + str(datetime.datetime.now())
     print "TOPICO: ",msg.topic,"payload: ",str(Payload)
     gravar_dado("home.csv",str(msg.topic),Payload,0)
   
    if "home/sala/porta/01/status/" in msg.topic:
     Payload = str(msg.payload) + str(datetime.datetime.now())
     print "TOPICO: ",msg.topic,"payload: ",str(Payload)
     gravar_dado("passagem.csv",str(msg.topic),Payload,0)
   
    if "home/sala/luminosidade/01/status/" in msg.topic: 
     Payload = str(msg.payload) + str(datetime.datetime.now())
     print "TOPICO: ",msg.topic,"payload: ",str(Payload)
     gravar_dado("luminosidade.csv",str(msg.topic),Payload,1)
<<<<<<< HEAD
=======
 
>>>>>>> eb23d16fd79c82247943502c318d00d4766771fb


# clia um cliente para supervisã0
client = mqtt.Client()

# estabelece as funçõe de conexão e mensagens
client.on_connect = on_connect
client.on_message = on_message

# conecta no broker
<<<<<<< HEAD
client.connect("192.168.100.10", 1883)
=======
client.connect("192.168.43.32", 1883)
>>>>>>> eb23d16fd79c82247943502c318d00d4766771fb

# permace em loop, recebendo mensagens
client.loop_forever()
