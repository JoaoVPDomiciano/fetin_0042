import sqlite3
import os
from datetime import datetime, timedelta
import requests
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise EnvironmentError("SUPABASE_URL ou SUPABASE_KEY não estão definidos no .env!")

DB_PATH = "../resultados_LOG.db"
TABLE_NAME = "resultados_LOG"

RETENTION_POLICY = {
    "INFO": 1,
    "WARNING": 3,
    "ERROR": 7,
    "CRITICAL": 14
}

def clean_supabase_table(table):
    url = f"{SUPABASE_URL}/rest/v1/{table}?select=id&order=timestamp.desc"
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}"
    }
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"[ERRO] ao buscar registros: {response.status_code} - {response.text}")
        return

    data = response.json()
    if len(data) <= 100:
        return  # Nada a limpar

    ids_a_excluir = [str(row["id"]) for row in data[100:]]

    delete_url = f"{SUPABASE_URL}/rest/v1/{table}?id=in.({','.join(ids_a_excluir)})"
    delete_headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json"
    }

    del_response = requests.delete(delete_url, headers=delete_headers)
    if del_response.status_code not in [200, 204]:
        print(f"[ERRO] ao deletar registros antigos: {del_response.status_code} - {del_response.text}")

def clean_logs_data():
    if not os.path.exists(DB_PATH):
        print(f"[ERRO] Banco de dados não encontrado em: {DB_PATH}")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Verifica se a tabela existe
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (TABLE_NAME,))
    if not cursor.fetchone():
        print(f"[ERRO] Tabela '{TABLE_NAME}' não existe.")
        conn.close()
        return

    now = datetime.now()

    for nivel, dias in RETENTION_POLICY.items():
        limite = now - timedelta(days=dias)
        cursor.execute(f"""
            DELETE FROM {TABLE_NAME}
            WHERE nivel = ? AND timestamp < ?
        """, (nivel, limite.isoformat()))
        print(f"[INFO] Logs '{nivel}' anteriores a {dias} dias removidos.")

    conn.commit()

    # Opcional: criar nova tabela ordenada (se desejar realmente sobrescrever dados antigos)
    cursor.execute(f"""
        CREATE TEMP TABLE ordered_logs AS
        SELECT * FROM {TABLE_NAME} ORDER BY nivel ASC
    """)
    cursor.execute(f"DELETE FROM {TABLE_NAME}")
    cursor.execute(f"""
        INSERT INTO {TABLE_NAME} (id, timestamp, mensagem, nivel, origem, evento_id)
        SELECT id, timestamp, mensagem, nivel, origem, evento_id FROM ordered_logs
    """)
    conn.commit()

    conn.close()
    print(f"[OK] Banco de dados local '{TABLE_NAME}' limpo e reordenado com sucesso.")

    clean_supabase_table("logs")