 
import numpy as np
import pandas as pd
from random import shuffle
from flask import Flask,render_template,request 
import pygal  
from pygal.style import DarkStyle
# "bloco/E/lab/302/SENSOR/JANELA/1"
def entrada():
 passagem = pd.read_csv('passagem.csv')
 tamanho = len(passagem)
 atual = (np.array(passagem[tamanho-1:tamanho]).tolist())[0]
 dados = atual
 passagem = {
 "Ambiente":dados[0],
 "IoT":dados[1],
 "ID":dados[2],
 "status": dados[3],
  "Data":dados[4],"Hora":dados[5]
 }
 return passagem

def luminosidade():
 luz = pd.read_csv('luminosidade.csv')
 tamanho = len(luz)
 atual = (np.array(luz[tamanho-1:tamanho]).tolist())[0]
 dados = atual
 luz = {"Ambiente":dados[0],
 "IoT":dados[1],
 "ID":dados[2],
 "status": "Ligada " if int(dados[3]) == 1 else "Desligada",
 "Data":dados[4],"Hora":dados[5]}
 return luz


def windows():
 janela = pd.read_csv('home.csv')
 leitura2 = len(janela)
 atual2 = (np.array(janela[leitura2-1:leitura2]).tolist())[0]
 dados = atual2
 janela = {"Ambiente":dados[0],
 "IoT":dados[1],"ID":dados[2],
 "status": 'Fechado 'if  int(dados[3]) == 1 else 'Aberto',"Data":dados[4],"Hora":dados[5]}
 return janela
 
def query_20(ID,p,dataset):
    df = pd.read_csv(dataset)
    query = df.iloc[len(df)-p:len(df)]
    ID = (query['ID'] == ID).tolist()
    return query[ID]

 
app = Flask(__name__)

@app.route("/")
def index():
	Windows = windows()
	Luminosidade = luminosidade()
	Porta = entrada()
	return render_template('index.html', janela=Windows,luminosidade=Luminosidade,door=Porta)

@app.route("/graph.html")
def graph():
    bar_chart = pygal.Line(style=DarkStyle,height=200)
    bar_chart.title = "Sensores"
    #bar_chart.x_labels = map(str, range(200))
    bar_chart.add('Luminosidade', query_20(1,30,"luminosidade.csv")[" STATUS "].values.tolist())
    bar_chart.add('Porta', query_20(1,200,"passagem.csv")[" STATUS "].values.tolist()) 
    bar_chart.add('Janela', query_20(1,200,"home.csv")[" STATUS "].values.tolist())  
    chart = bar_chart.render(is_unicode=True)
    return render_template('graph.html', chart=chart)


@app.route("/system.html")
def system():
	return render_template('system.html')


if __name__=="__main__":
	app.run(host="0.0.0.0",port=8080,debug=True)
