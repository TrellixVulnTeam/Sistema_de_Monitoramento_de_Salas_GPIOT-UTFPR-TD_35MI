 
import numpy as np
import pandas as pd
from flask import Flask,render_template,request 
  
# "bloco/E/lab/302/SENSOR/JANELA/1"
def atual():
 df = pd.read_csv('home.csv')
 leitura = len(df)
 atual = (np.array(df[leitura-1:leitura]).tolist())[0]
 dados = atual
 parametro = {
"Ambiente":dados[0],
"IoT":dados[1],
"ID":dados[2],
"status":dados[3],
"Data":dados[4],
"Hora":dados[5]
}

 return parametro

print atual() 
 

app = Flask(__name__)

@app.route("/")
def index():
	parametro = atual()
	return render_template('index.html', parametro=parametro)

if __name__=="__main__":
	app.run(host="0.0.0.0",port=8080,debug=True)
