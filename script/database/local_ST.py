import sqlite3

DB_PATH_ST = "resultados_ST.db"

def criar_tabela_speedTest():
    conn = sqlite3.connect(DB_PATH_ST)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS resultados_ST (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ping TEXT,
            download REAL,
            upload REAL,
            timestamp TEXT,
            enviado INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()

def salvar_sqlite_speedTest(dados):
    conn = sqlite3.connect(DB_PATH_ST)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM resultados_ST")
    total = cursor.fetchone()[0]

    if total >= 500:
        print("♻️ Rotação de dados do SpeedTest: apagando todos os registros antigos...")
        cursor.execute("DELETE FROM resultados_ST")

    cursor.execute("""
        INSERT INTO resultados_ST (ping, download, upload, timestamp)
        VALUES (?, ?, ?, ?)
    """, (dados["ping"], dados["download"], dados["upload"], dados["timestamp"]))

    conn.commit()
    conn.close()