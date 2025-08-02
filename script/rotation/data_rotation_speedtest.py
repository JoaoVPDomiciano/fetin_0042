import sqlite3
import os
import requests
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

DB_PATH = "../resultados_ST.db"
TABLE_NAME = "resultados_ST"

def clean_supabase_table(table):
    url = f"{SUPABASE_URL}/rest/v1/{table}?id=lt.0"
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json"
    }
    response = requests.delete(url, headers=headers)
    if response.status_code not in [200, 204]:
        print(f"[ERRO] ao limpar Supabase: {response.status_code} - {response.text}")

def clean_speedtest_data():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(f"SELECT COUNT(*) FROM {TABLE_NAME}")
    total = cursor.fetchone()[0]

    if total > 100:
        excess = total - 100
        cursor.execute(f"DELETE FROM {TABLE_NAME} WHERE id IN (SELECT id FROM {TABLE_NAME} ORDER BY timestamp ASC LIMIT ?)", (excess,))
        conn.commit()

        cursor.execute(f"CREATE TABLE IF NOT EXISTS temp AS SELECT * FROM {TABLE_NAME} ORDER BY timestamp ASC")
        cursor.execute(f"DROP TABLE {TABLE_NAME}")
        cursor.execute(f"ALTER TABLE temp RENAME TO {TABLE_NAME}")
        conn.commit()

    conn.close()
    clean_supabase_table("speedtest")