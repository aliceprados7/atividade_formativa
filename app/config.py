import os

DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_USER = os.getenv("DB_USER", "app_user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "app_pass")
DB_NAME = os.getenv("DB_NAME", "cadastro_clientes")

SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "chave")
FLASK_DEBUG = os.getenv("FLASK_DEBUG", "1") == "1"
