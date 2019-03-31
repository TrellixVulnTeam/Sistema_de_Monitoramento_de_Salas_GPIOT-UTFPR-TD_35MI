# -*- coding: utf-8 -*-

import sys
import time
import telepot
from telepot.loop import MessageLoop
import numpy as np
import pandas as pd

std = """Oi, sou um bot para reserva de labs da UTFPR-TOLEDO do Grupo de pesquisa de Internet das Coisas, estou em fase de desenvolvimento por fazer converse comigo para que eu possa aprender com você, para reservar sala ou solicitar  sala me fale qual sala e dia tem interesse. Que já lhe digo qual sala vai estar disponivel Ok ? """


def entrada():
 passagem = pd.read_csv('../mqtt/passagem.csv')
 tamanho = len(passagem)
 atual = (np.array(passagem[tamanho-1:tamanho]).tolist())[0]
 dados = atual
 passagem = """
 Ambiente: %s
 IoT: %s
 ID: %s
 status:  %s
 Data:  %s
 Hora: %s""" % (dados[0],dados[1],dados[2],dados[3],dados[4],dados[5])
 return passagem

def luminosidade():
 luz = pd.read_csv('../mqtt/luminosidade.csv')
 tamanho = len(luz)
 atual = (np.array(luz[tamanho-1:tamanho]).tolist())[0]
 dados = atual
 luz = """
 Ambiente: %s
 IoT: %s
 ID: %s
 status:  %s
 Data:  %s
 Hora: %s""" % (dados[0],dados[1],dados[2],dados[3],dados[4],dados[5])
 return luz


def windows():
 janela = pd.read_csv('../mqtt/home.csv')
 leitura2 = len(janela)
 atual2 = (np.array(janela[leitura2-1:leitura2]).tolist())[0]
 dados = atual2
 janela = {"Ambiente":dados[0],"IoT":dados[1],"ID":dados[2],"status": 'Fechado 'if  int(dados[3]) == 1 else 'Aberto',"Data":dados[4],"Hora":dados[5]}
 janela = """
 Ambiente: %s
 IoT: %s
 ID: %s
 status:  %s
 Data:  %s
 Hora: %s""" %  ((dados[0],dados[1],dados[2],'Fechado 'if  int(dados[3]) == 1 else 'Aberto',dados[4],dados[5]))
 return janela
 





def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    print(content_type, chat_type, chat_id)
    
    if content_type == 'text':
    	print msg['text']
    	if msg['text'] == "Oi":
          bot.sendMessage(chat_id, std)
        if msg['text'] == "/luminosidade":
          bot.sendMessage(chat_id, "Buscando dado no banco....")
          bot.sendMessage(chat_id, luminosidade())
        if msg['text'] == "/porta":
          bot.sendMessage(chat_id, "Buscando dado no banco....")
          bot.sendMessage(chat_id, entrada())
        if msg['text'] == "/janela":
          bot.sendMessage(chat_id, "Buscando dado no banco....")
          bot.sendMessage(chat_id, windows())
       


#TOKEN = sys.argv[1]  # get token from command-line

bot = telepot.Bot('****TOKEN**')
MessageLoop(bot, handle).run_as_thread()
print ('Listening ...')

# Keep the program running.
while 1:
    time.sleep(10)
