import sqlite3
import os
import requests
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise EnvironmentError("SUPABASE_URL ou SUPABASE_KEY não estão definidos no .env!")

DB_PATH = "../resultados_TRAFFIC.db"
TABLE_NAME = "resultados_TRAFFIC"

def clean_supabase_table(table):
    url = f"{SUPABASE_URL}/rest/v1/{table}?id=gt.0"
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=minimal"
    }
    response = requests.delete(url, headers=headers)
    if response.status_code not in [200, 204]:
        print(f"[ERRO] ao limpar Supabase: {response.status_code} - {response.text}")
    else:
        print(f"[OK] Supabase '{table}' limpa com sucesso.")

def clean_trafego_data():
    if not os.path.exists(DB_PATH):
        print(f"[ERRO] Banco de dados não encontrado: {DB_PATH}")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Verifica se a tabela existe
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (TABLE_NAME,))
    if not cursor.fetchone():
        print(f"[ERRO] Tabela '{TABLE_NAME}' não existe.")
        conn.close()
        return

    cursor.execute(f"SELECT COUNT(*) FROM {TABLE_NAME}")
    total = cursor.fetchone()[0]

    if total > 100:
        excess = total - 100
        print(f"[INFO] Removendo {excess} registros mais antigos de '{TABLE_NAME}'...")

        cursor.execute(f"""
            DELETE FROM {TABLE_NAME}
            WHERE id IN (
                SELECT id FROM {TABLE_NAME}
                ORDER BY timestamp ASC
                LIMIT ?
            )
        """, (excess,))
        conn.commit()

        # Reorganiza os dados restantes por timestamp
        cursor.execute(f"""
            CREATE TEMP TABLE temp_ordered AS
            SELECT * FROM {TABLE_NAME} ORDER BY timestamp ASC
        """)
        cursor.execute(f"DELETE FROM {TABLE_NAME}")
        cursor.execute(f"""
            INSERT INTO {TABLE_NAME} (
                id, timestamp, interface, bytes_enviados, bytes_recebidos
            )
            SELECT id, timestamp, interface, bytes_enviados, bytes_recebidos FROM temp_ordered
        """)
        conn.commit()
        print(f"[OK] Tabela '{TABLE_NAME}' reorganizada com sucesso.")
    else:
        print(f"[INFO] Nenhuma limpeza necessária. Total de registros: {total}")

    conn.close()
    clean_supabase_table("trafego")
