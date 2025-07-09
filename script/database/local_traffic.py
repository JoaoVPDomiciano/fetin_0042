import sqlite3

DB_PATH_TRAFFIC = "resultados_TRAFFIC.db"

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
