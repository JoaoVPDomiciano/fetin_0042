import sqlite3

DB_PATH_LOGS = "../resultados_LOG.db"

def criar_tabela_logs():
    conn = sqlite3.connect(DB_PATH_LOGS)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS resultados_LOG (
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
        INSERT INTO resultados_LOG (timestamp, mensagem, nivel, origem, evento_id)
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
