import threading
import requests
import random
import time
from flask import Flask, render_template, request, url_for, flash, jsonify
from flask_cors import CORS
from banco import conectar
from config import SECRET_KEY, FLASK_DEBUG

API_KEY = "ZXCK40DOE70O40AW"


def writeThingSpeak():
    """Loop infinito que envia dados aleatórios a cada 15 segundos"""
    while True:
        temperatura = round(random.uniform(20, 30), 2)
        umidade = round(random.uniform(50, 70), 2)
        
        url = f"https://api.thingspeak.com/update?api_key={API_KEY}&field1={temperatura}&field2={umidade}"
        try:
            reposta = requests.get(url)
            print(f"[Thread Envio] Dados enviados: T={temperatura}, U={umidade} | Status: {reposta.text}")
        except Exception as e:
            print(f"[Thread Envio] Erro ao enviar: {e}")
            
        time.sleep(15)

def readThingSpeak():
    channel_id = 3305425
    num_results = 10
    url = f"https://api.thingspeak.com/channels/3305425/feeds.json?results=10"

    response = requests.get(url)
    dados_processados = []

    if response.status_code == 200:
        data = response.json()
        feeds = data['feeds']
        conexao = conectar()
        cursor = conexao.cursor()

        for registro in feeds:
            temp = registro['field1']
            umid = registro['field2']
            dt_hr = registro['created_at'].replace('T', ' ').replace('Z', '')

            try:
                cursor.execute(
                    "INSERT INTO registros (data_hora, temperatura, umidade, origem_dado) VALUES (%s, %s, %s, %s)",
                    (dt_hr, temp, umid, "ThingSpeak")
                )
                dados_processados.append({
                    "data_hora": dt_hr, "temperatura": temp, "umidade": umid, "origem": "ThingSpeak"
                })
            except Exception as e:
                print(f"Erro no banco: {e}")

        conexao.commit()
        cursor.close()
        conexao.close()
        return dados_processados
    return []


app = Flask(__name__)
CORS(app)
app.secret_key = SECRET_KEY

@app.get("/")
def listar_dados():
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)
    cursor.execute("SELECT id, data_hora, umidade, temperatura FROM registros ORDER BY id DESC LIMIT 20")
    dados = cursor.fetchall()
    
    for d in dados:
        d['data_hora'] = str(d['data_hora'])
        
    cursor.close()
    conexao.close()
    return jsonify({"dados": dados})

@app.get("/dados")
def listar_dados_ts():
    dados_lidos = readThingSpeak()
    if dados_lidos:
        return jsonify({"status": "sucesso", "dados": dados_lidos}), 200
    return jsonify({"status": "erro", "mensagem": "Sem novos dados"}), 404


if __name__ == "__main__":
    tarefa_envio = threading.Thread(target=writeThingSpeak, daemon=True)
    tarefa_envio.start()

    app.run(host="0.0.0.0", port=5000, debug=FLASK_DEBUG)