import subprocess
import json
from datetime import datetime

PALAVRAS_CHAVE = [
    'falha', 'erro', 'fail', 'timeout', 'restart', 'dhcp',
    'ip', 'dns', 'driver', 'desconectado', 'conexão', 'conectado'
]

def coletar_logs(linhas=10):
    comando = [
        "journalctl",
        "-n", str(linhas),
        "--no-pager",
        "--output", "json"
    ]

    try:
        resultado = subprocess.run(comando, capture_output=True, text=True, timeout=10)
        if resultado.returncode != 0:
            print("[ERRO] Falha ao executar journalctl:", resultado.stderr)
            return []

        logs_filtrados = []

        for linha in resultado.stdout.strip().split("\n"):
            try:
                log = json.loads(linha)
                log_entry = {
                    "timestamp": converter_timestamp(log.get("__REALTIME_TIMESTAMP")),
                    "nivel": log.get("PRIORITY", "N/A"),
                    "origem": log.get("_SYSTEMD_UNIT", log.get("SYSLOG_IDENTIFIER", "Desconhecido")),
                    "evento_id": log.get("MESSAGE_ID", "N/A"),
                    "mensagem": log.get("MESSAGE", "Sem mensagem")
                }

                if any(palavra in log_entry["mensagem"].lower() for palavra in PALAVRAS_CHAVE):
                    logs_filtrados.append(log_entry)

            except json.JSONDecodeError:
                continue

        return logs_filtrados

    except Exception as e:
        print(f"[ERRO] Exceção ao coletar logs: {e}")
        return []

def converter_timestamp(timestamp_str):
    try:
        microssegundos = int(timestamp_str)
        segundos = microssegundos / 1_000_000
        return datetime.utcfromtimestamp(segundos).isoformat() + 'Z'
    except (ValueError, TypeError):
        return datetime.utcnow().isoformat() + 'Z'