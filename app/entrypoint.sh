#!/bin/sh
set -e

echo "[ENTRYPOINT] Aguardando MySQL ficar pronto..."
python wait_for_db.py

echo "[ENTRYPOINT] Iniciando Flask..."
python app.py

