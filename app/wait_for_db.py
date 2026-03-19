import time
import sys
import mysql.connector

from config import DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME

def tentar_conectar():

    conexao = mysql.connector.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

    conexao.close()

if __name__ == "__main__":
    max_tentativas = 30

    intervalo = 2

    for tentativa in range (1, max_tentativas + 1):

        try:
            print(f"[wait_for_db] Tentativa {tentativa}/{max_tentativas} conectando no MySQL...")

            tentar_conectar()

            print("[wait_for_db] MySQL disponível!")

            sys.exit(0)

        except Exception as e:
            print(f"[wait_for_db] MySQL ainda não disponível: {e}")

            time.sleep(intervalo)

    print("[wait_for_db] Falha: MySQL não ficou disponível a tempo.")

    sys.exit(1)
    