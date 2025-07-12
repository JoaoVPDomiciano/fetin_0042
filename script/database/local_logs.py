import sqlite3

from .data_rotator import clean_sqlite_table, clean_supabase_table
DB_PATH_LOGS = "resultados_LOG.db"  # Caminho do banco de dados local
TABLE_NAME = "resultados_LOG"

def criar_tabela_logs():
    conn = sqlite3.connect(DB_PATH_LOGS)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            mensagem TEXT,
            nivel TEXT,
            origem TEXT,
            evento_id TEXT
        )
    """)
    conn.commit()
    conn.close()

def salvar_sqlite_logs(log):
    conn = sqlite3.connect(DB_PATH_LOGS)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO logs (timestamp, mensagem, nivel, origem, evento_id)
        VALUES (?, ?, ?, ?, ?)
    """, (
        log.get("timestamp"),
        log.get("mensagem"),
        log.get("nivel"),
        log.get("origem"),
        log.get("evento_id")
    ))
    conn.commit()
    conn.close()

    clean_sqlite_table(DB_PATH_LOGS, TABLE_NAME)
    clean_supabase_table("logs")
