import sqlite3
import os
from datetime import datetime, timedelta
import requests
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

DB_PATH = "resultados_LOG.db"
TABLE_NAME = "resultados_LOG"

RETENTION_POLICY = {
    "INFO": 1,
    "WARNING": 3,
    "ERROR": 7,
    "CRITICAL": 14
}

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

def clean_logs_data():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    now = datetime.now()

    for nivel, dias in RETENTION_POLICY.items():
        limite = now - timedelta(days=dias)
        cursor.execute(f"DELETE FROM {TABLE_NAME} WHERE nivel=? AND timestamp < ?", (nivel, limite.isoformat()))

    conn.commit()

    cursor.execute(f"CREATE TABLE IF NOT EXISTS temp AS SELECT * FROM {TABLE_NAME} ORDER BY timestamp ASC")
    cursor.execute(f"DROP TABLE {TABLE_NAME}")
    cursor.execute(f"ALTER TABLE temp RENAME TO {TABLE_NAME}")
    conn.commit()

    conn.close()
    clean_supabase_table("logs")