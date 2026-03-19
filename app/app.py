# imports
import requests
import random
import time
from flask import Flask, render_template, request, url_for, flash, jsonify

from banco import conectar

from config import SECRET_KEY, FLASK_DEBUG

API_KEY= "ZXCK40DOE70O40AW"

def writeThingSpeak(temperatura, umidade):
    url = f"https://api.thingspeak.com/update?api_key={API_KEY}&field1={temperatura}&field2={umidade}"

    reposta = requests.get(url)

    print("Temperatura enviada:", temperatura)
    print("Umidade enviada:", umidade)

    print("Resposta da API:", reposta.text)

def readThingSpeak():
    channel_id = 3305425
    num_results = 10
    url = f"https://api.thingspeak.com/channels/{channel_id}/feeds.json?results={num_results}"

    response = requests.get(url)
    
    dados_processados = []

    if response.status_code == 200:
        data = response.json()
        feeds = data['feeds']

        conexao = conectar()
        cursor = conexao.cursor()

        for registro in feeds:
            temperatura = registro['field1']
            umidade = registro['field2']
            data_hora = registro['created_at'].replace('T', ' ').replace('Z', '')

            try:
                cursor.execute(
                    "INSERT INTO registros (data_hora, temperatura, umidade, origem_dado) VALUES (%s, %s, %s, %s)",
                    (data_hora, temperatura, umidade, "ThingSpeak")
                )

                dados_processados.append({
                    "data_hora": data_hora,
                    "temperatura": temperatura,
                    "umidade": umidade,
                    "origem": "ThingSpeak"
                })
                
            except Exception as e:
                print(f"Erro ao inserir registro: {e}")

        conexao.commit()
        cursor.close()
        conexao.close()

        return dados_processados

    else:
        print(f"Erro ao acessar ThingSpeak: {response.status_code}")
        return [] 

app = Flask(__name__)

app.secret_key = SECRET_KEY

@app.get("/")
def listar_dados():
    conexao = conectar()

    cursor = conexao.cursor(dictionary=True)

    cursor.execute(
        "SELECT id, data_hora, umidade, temperatura FROM registros ORDER BY id ASC"
    )

    dados = cursor.fetchall()

    cursor.close()
    conexao.close()

    return jsonify({
        dados
    })

@app.get("/dados")
def listar_dados_ts():
    dados_lidos = readThingSpeak()

    if dados_lidos:
        return jsonify({
            "status": "sucesso",
            "quantidade": len(dados_lidos),
            "dados": dados_lidos
        }), 200
    else:
        return jsonify({
            "status": "erro",
            "mensagem": "Nenhum dado encontrado ou erro na API"
        }), 404

while True:

    temperatura = round(random.uniform(20,30),2)

    umidade = round(random.uniform(50,70),2)

    writeThingSpeak(temperatura, umidade)

    time.sleep(15)