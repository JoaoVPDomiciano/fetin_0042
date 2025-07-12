import sqlite3

from .data_rotator import clean_sqlite_table, clean_supabase_table
DB_PATH_TRAFFIC = "resultados_TRAFFIC.db"
TABLE_NAME = "trafego"


def criar_tabela_trafego():
    conn = sqlite3.connect(DB_PATH_TRAFFIC)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS trafego (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            porta INTEGER,
            tipo TEXT
        )
    """)
    conn.commit()
    conn.close()

def salvar_sqlite_trafego(pacote):
    conn = sqlite3.connect(DB_PATH_TRAFFIC)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO trafego (timestamp, porta, tipo)
        VALUES (?, ?, ?)
    """, (pacote["timestamp"], pacote["porta"], pacote["tipo"]))
    conn.commit()
    conn.close()

    clean_sqlite_table(DB_PATH_TRAFFIC, TABLE_NAME)
    clean_supabase_table("speedtest")