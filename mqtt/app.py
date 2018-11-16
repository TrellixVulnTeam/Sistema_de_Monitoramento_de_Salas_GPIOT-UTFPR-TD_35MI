 
import numpy as np
import pandas as pd
from flask import Flask,render_template,request 
  
# "bloco/E/lab/302/SENSOR/JANELA/1"
def atual():
 janela = pd.read_csv('home.csv')
 passagem = pd.read_csv('passagem.csv')
 leitura = len(janela)
 leitura2 = len(passagem)
 atual = (np.array(janela[leitura-1:leitura]).tolist())[0]
 atual2 = (np.array(passagem[leitura2-1:leitura2]).tolist())[0]
 dados = atual
 dados1 = atual2
 passagem = {
"Ambiente":dados1[0],
"IoT":dados1[1],
"ID":dados1[2],
"status": "%.2f %.2f" % (float(dados1[3].split()[0]),float(dados1[3].split()[1])),
"Data":dados1[4],
"Hora":dados1[5]
     
 }   
 janela = {
"Ambiente":dados[0],
"IoT":dados[1],
"ID":dados[2],
"status": 'Fechado 'if  int(dados[3]) == 1 else 'Aberto',
"Data":dados[4],
"Hora":dados[5]
}
 return janela,passagem




print atual() 
 

app = Flask(__name__)

@app.route("/")
def index():
	parametro = atual()[0]
	dado = atual()[1]
	return render_template('index.html', parametro=parametro,dado=dado)

if __name__=="__main__":
	app.run(host="0.0.0.0",port=8080,debug=True)
