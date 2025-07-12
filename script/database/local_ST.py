import sqlite3

from .data_rotator import clean_sqlite_table, clean_supabase_table
DB_PATH_ST = "resultados_ST.db"
TABLE_NAME = "resultados_ST"

def criar_tabela_speedTest():
    conn = sqlite3.connect(DB_PATH_ST)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS resultados_ST (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ping TEXT,
            download REAL,
            upload REAL,
            timestamp TEXT
            enviado INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()

def salvar_sqlite_speedTest(dados):
    conn = sqlite3.connect(DB_PATH_ST)
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO resultados_ST (ping, download, upload, timestamp)
        VALUES (?, ?, ?, ?)
    ''', (dados["ping"], dados["download"], dados["upload"], dados["timestamp"]))

    conn.commit()
    conn.close()

    clean_sqlite_table(DB_PATH_ST, TABLE_NAME)
    clean_supabase_table("speedtest")