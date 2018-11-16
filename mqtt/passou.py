import pandas as pd 
import numpy as np
import time as tmp 


def escreve_file(value1,value2):
   arq = open('log.txt', 'w')
   texto = "Passagem"
   if value1 == 1 and value2==0:
     texto =  "Passagem  %s  Passou"  % (value1 + value2)
   if value1 == 0 and value2==2: 
     texto =  "Passagem  %s  Passou"  % (value1 + value2)  
   print texto
   arq.write(texto)
   arq.close()


while True:
 init = 0
 fim = 0
 df = pd.read_csv("passagem.csv")
 leitura = len(df)
 sensores = []
 for p in range(20):
  data = np.array(df[leitura-20:leitura]).tolist()[p]
  sensores.append(data[3])
 s1 = []
 s2 = []
 for p in range(len(sensores)):
    s1.append(sensores[p].split()[0])
    s2.append(sensores[p].split()[1])
 
 if float(s1[10]) < 20:
        init = 1
        
 if float(s2[19]) < 20:
        fim = 2

 escreve_file(init,fim)