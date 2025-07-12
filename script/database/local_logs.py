import sqlite3
import os

DB_PATH_LOGS = "resultados_LOG.db"
TABELA = "logs"

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

    cursor.execute(f"SELECT COUNT(*) FROM {TABELA}")
    total = cursor.fetchone()[0]

    if total >= 500:
        print("♻️ Rotação de logs: apagando os mais antigos...")
        cursor.execute(f"""
            DELETE FROM {TABELA}
            WHERE id NOT IN (
                SELECT id FROM {TABELA} ORDER BY id DESC LIMIT 500
            )
        """)

    cursor.execute(f"""
        INSERT INTO {TABELA} (timestamp, mensagem, nivel, origem, evento_id)
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

def limpar_banco_local(db_path):
    if not os.path.exists(db_path):
        print(f"[!] Banco não encontrado: {db_path}")
        return

    try:
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()

        cur.execute(f"SELECT id FROM {TABELA} ORDER BY id DESC LIMIT 1 OFFSET 499")
        resultado = cur.fetchone()

        if resultado:
            limite_id = resultado[0]
            cur.execute(f"DELETE FROM {TABELA} WHERE id < ?", (limite_id,))
            conn.commit()
            print(f"[OK] Limpou dados antigos em: {db_path}")
        else:
            print(f"[OK] Menos de 500 registros em: {db_path}")

        conn.close()

    except Exception as e:
        print(f"[ERRO] Erro ao limpar {db_path}: {e}")
