import speedtest
import subprocess
import platform
from datetime import datetime
import sqlite3

from script.database.data_rotator import clean_sqlite_table, clean_supabase_table
from script.database.local_ST import DB_PATH_ST

def obter_comando_ping():
    return ['ping', '-n', '4', '8.8.8.8'] if platform.system() == "Windows" else ['ping', '-c', '4', '8.8.8.8']

def testar_conexao():
    st = speedtest.Speedtest()

    try:
        resultado_ping = subprocess.run(
            obter_comando_ping(),
            capture_output=True,
            text=True,
            timeout=10
        )
        ping = resultado_ping.stdout if resultado_ping.returncode == 0 else "Erro no ping"
    except Exception as e:
        ping = f"Erro ao executar ping: {e}"

    try:
        download = st.download() / 1_000_000
        upload = st.upload() / 1_000_000
    except Exception as e:
        print(f"[ERRO] Speedtest falhou: {e}")
        download = upload = 0

    return {
        "ping": ping,
        "download": round(download, 2),
        "upload": round(upload, 2),
        "timestamp": datetime.now().isoformat()
    }

local_conn = sqlite3.connect(DB_PATH_ST)
clean_sqlite_table(local_conn, "resultados_ST")
clean_supabase_table("speedtest")
local_conn.close()