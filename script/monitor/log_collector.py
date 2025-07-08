import subprocess
import platform
import json
from datetime import datetime

PALAVRAS_CHAVE = [
    'falha', 'erro', 'fail', 'timeout', 'restart', 'dhcp',
    'ip', 'dns', 'driver', 'desconectado', 'conexão', 'conectado'
]

def formatar_timestamp_windows(valor):
    try:
        return datetime.strptime(valor, "%m/%d/%Y %I:%M:%S %p").isoformat()
    except Exception:
        if isinstance(valor, str) and valor.startswith("/Date("):
            millis = int(valor.strip("/Date()").split("+")[0])
            dt = datetime.utcfromtimestamp(millis / 1000)
            return dt.isoformat()
        return datetime.now().isoformat()

def coletar_logs(linhas=10):
    sistema = platform.system()

    if sistema == "Linux":
        return coletar_logs_linux(linhas)
    elif sistema == "Windows":
        return coletar_logs_windows(linhas)
    else:
        print("[ERRO] Sistema não suportado para coleta de logs.")
        return []

def coletar_logs_linux(linhas=10):
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

        logs = []
        for linha in resultado.stdout.strip().split("\n"):
            try:
                log = json.loads(linha)
                log_entry = {
                    "timestamp": datetime.utcfromtimestamp(
                        int(log.get("__REALTIME_TIMESTAMP", "0")) / 1_000_000
                    ).isoformat() if "__REALTIME_TIMESTAMP" in log else datetime.now().isoformat(),
                    "nivel": log.get("PRIORITY", "N/A"),
                    "origem": log.get("_SYSTEMD_UNIT", log.get("SYSLOG_IDENTIFIER", "Desconhecido")),
                    "evento_id": log.get("MESSAGE_ID", "N/A"),
                    "mensagem": log.get("MESSAGE", "Sem mensagem")
                }
                logs.append(log_entry)
            except json.JSONDecodeError:
                continue

        return [
            log for log in logs
            if any(p.lower() in log["mensagem"].lower() for p in PALAVRAS_CHAVE)
        ]

    except Exception as e:
        print(f"[ERRO] Exceção ao coletar logs no Linux: {e}")
        return []

def coletar_logs_windows(linhas=10):
    comando = [
        "powershell",
        "-Command",
        f"Get-EventLog -LogName System -Newest {linhas} | "
        "Select-Object TimeGenerated, EntryType, Source, EventID, Message | ConvertTo-Json"
    ]

    try:
        resultado = subprocess.run(
            comando,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='ignore',
            timeout=10
        )

        if resultado.returncode != 0:
            print("[ERRO] Falha ao executar PowerShell:", resultado.stderr)
            return []

        output = resultado.stdout.strip()
        if not output:
            print("[ERRO] PowerShell retornou saída vazia")
            return []

        logs = json.loads(output)
        if isinstance(logs, dict):
            logs = [logs]

        logs_formatados = []
        for log in logs:
            logs_formatados.append({
                "timestamp": formatar_timestamp_windows(log.get("TimeGenerated")),
                "nivel": log.get("EntryType", "N/A"),
                "origem": log.get("Source", "Desconhecido"),
                "evento_id": log.get("EventID", "N/A"),
                "mensagem": log.get("Message", "Sem mensagem")
            })

        return [
            log for log in logs_formatados
            if any(p.lower() in log["mensagem"].lower() for p in PALAVRAS_CHAVE)
        ]

    except Exception as e:
        print(f"[ERRO] Exceção ao coletar logs no Windows: {e}")
        return []
