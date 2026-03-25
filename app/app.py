# importações
import threading
import requests
import random
import time
from flask import Flask, render_template, request, url_for, flash, jsonify
from flask_cors import CORS
from banco import conectar
from config import SECRET_KEY, FLASK_DEBUG

# chave ThingSpeak
API_KEY = "ZXCK40DOE70O40AW"

# função que simula dados coletados a cada 15 segundos
# função de escrita no ThingSpeak
def writeThingSpeak():
    while True:
        # dados simulados de forma randomica
        temperatura = round(random.uniform(20, 30), 2)
        umidade = round(random.uniform(50, 70), 2)
        # url de escrita da plataforma
        url = f"https://api.thingspeak.com/update?api_key={API_KEY}&field1={temperatura}&field2={umidade}"
        try:
            reposta = requests.get(url)
            print(f"Dados enviados: T={temperatura}, U={umidade} | Status: {reposta.text}")
        except Exception as e:
            print(f"Erro ao enviar: {e}")
        # tempo de espera
        time.sleep(15)

# função que lê os dados do ThingSpeak
def readThingSpeak():
    # id do canal, número de resultados esperados e url da plataforma
    channel_id = 3305425
    num_results = 10
    url = "https://api.thingspeak.com/channels/{}/feeds.json?results={}".format(channel_id, num_results)

    response = requests.get(url)
    dados_processados = []
    # caso busca bem sucedidda
    if response.status_code == 200:
        data = response.json()
        # a plataforma envia dados nomeados de feeeds
        # "feeds": [
        # {
        #   "created_at": "2026-03-25T22:37:35Z",
        #   "entry_id": 429,
        #   "field1": "21.64",
        #   "field2": "62.61"
        # },
        feeds = data['feeds']

        # abrindo conexão com o banco
        conexao = conectar()
        cursor = conexao.cursor()
        # percorrendo os feeds enviados
        for registro in feeds:
            temp = registro['field1']
            umid = registro['field2']
            # adequando a data conforme o banco de dados
            dt_hr = registro['created_at'].replace('T', ' ').replace('Z', '')

            try:
                # inserindo valores no banco
                cursor.execute(
                    "INSERT INTO registros (data_hora, temperatura, umidade, origem_dado) VALUES (%s, %s, %s, %s)",
                    (dt_hr, temp, umid, "ThingSpeak")
                )
                # criando um json de dados recebidos
                dados_processados.append({
                    "data_hora": dt_hr, "temperatura": temp, "umidade": umid, "origem": "ThingSpeak"
                })
            except Exception as e:
                print(f"Erro no banco: {e}")
        # fechando conexão e enviando os dados
        conexao.commit()
        cursor.close()
        conexao.close()
        return dados_processados
    return []

# configurações de aplicações
app = Flask(__name__)
CORS(app)
app.secret_key = SECRET_KEY

# url responsável por buscar dados no banco e disponibilizar no localhost:5050
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

# url responsável por buscar dados do thingspeak e disponibilizar no localhost:5050/dados
@app.get("/dados")
def listar_dados_ts():
    dados_lidos = readThingSpeak()
    if dados_lidos:
        return jsonify({"status": "sucesso", "dados": dados_lidos}), 200
    return jsonify({"status": "erro", "mensagem": "Sem novos dados"}), 404


if __name__ == "__main__":
    # usando threading para rodar a aplicação e o while que envia dados para a plataforma
    # necessário pois são dois serviços em paralelo
    tarefa_envio = threading.Thread(target=writeThingSpeak, daemon=True)
    tarefa_envio.start()

    app.run(host="0.0.0.0", port=5000, debug=FLASK_DEBUG)