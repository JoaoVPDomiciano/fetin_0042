import sqlite3
import os
import requests
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

def clean_sqlite_table(db_path, table_name):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute(f'''
            DELETE FROM {table_name}
            WHERE id NOT IN (
                SELECT id FROM {table_name}
                ORDER BY id DESC
                LIMIT 100
            )
        ''')
        conn.commit()
        conn.close()
        print(f"[SQLite] Tabela '{table_name}' em '{db_path}' rotacionada.")
    except Exception as e:
        print(f"[SQLite] [ERRO] Erro ao limpar tabela '{table_name}': {e}")

def clean_supabase_table(table_name):
    try:
        url = f"{SUPABASE_URL}/rest/v1/{table_name}?select=id&order=id.desc&limit=100"
        response = requests.get(url, headers=HEADERS)

        if response.status_code != 200:
            print(f"[Supabase] [ERRO] Erro na busca: {response.status_code}")
            return

        ids = response.json()
        if not ids:
            print(f"[Supabase] [ERRO] Nenhum dado encontrado em '{table_name}'.")
            return

        min_id = min(row["id"] for row in ids)
        delete_url = f"{SUPABASE_URL}/rest/v1/{table_name}?id=lt.{min_id}"
        del_headers = {**HEADERS, "Prefer": "return=minimal"}

        del_response = requests.delete(delete_url, headers=del_headers)
        if del_response.status_code in [200, 204]:
            print(f"[Supabase] Tabela '{table_name}' rotacionada.")
        else:
            print(f"[Supabase][ERRO] Erro ao deletar: {del_response.status_code}")
    except Exception as e:
        print(f"[Supabase] [ERRO] Exceção ao limpar '{table_name}': {e}")
