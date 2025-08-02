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
            print("[ERRO] Não foi possível acessar os registros do sistema. Detalhes técnicos:", resultado.stderr)
            return []

        logs_filtrados = []

        for linha in resultado.stdout.strip().split("\n"):
            try:
                log = json.loads(linha)
                mensagem_bruta = log.get("MESSAGE", "").strip()

                if not mensagem_bruta:
                    continue

                if any(palavra in mensagem_bruta.lower() for palavra in PALAVRAS_CHAVE):
                    log_entry = {
                        "timestamp": converter_timestamp(log.get("__REALTIME_TIMESTAMP")),
                        "mensagem": humanizar_mensagem(mensagem_bruta),
                        "mensagem_original": mensagem_bruta,
                        "nivel": log.get("PRIORITY"),
                        "origem": log.get("SYSLOG_IDENTIFIER"),
                        "evento_id": log.get("MESSAGE_ID") or log.get("_PID")
                    }
                    logs_filtrados.append(log_entry)

            except json.JSONDecodeError:
                continue

        return logs_filtrados

    except Exception as e:
        print(f"[ERRO] Ocorreu um problema ao tentar coletar os registros do sistema. Motivo: {e}")
        return []

def humanizar_mensagem(mensagem):
    mensagem_lower = mensagem.lower()

    if "dns" in mensagem_lower:
        return "Problema ao resolver o endereço DNS. Pode indicar instabilidade na rede."
    elif "timeout" in mensagem_lower:
        return "Tempo limite excedido para uma operação de rede ou sistema."
    elif "fail" in mensagem_lower or "falha" in mensagem_lower:
        return "Falha detectada no sistema ou em um serviço."
    elif "erro" in mensagem_lower:
        return "Erro detectado em algum componente do sistema."
    elif "restart" in mensagem_lower:
        return "Reinício automático de um componente detectado."
    elif "dhcp" in mensagem_lower:
        return "Solicitação de IP via DHCP em andamento ou com erro."
    elif "ip" in mensagem_lower:
        return "Endereço IP alterado ou problema ao configurar IP."
    elif "driver" in mensagem_lower:
        return "Possível falha de driver. Verifique os dispositivos conectados."
    elif "desconectado" in mensagem_lower:
        return "Perda de conexão com a rede ou hardware."
    elif "conexão" in mensagem_lower:
        return "Alteração ou falha na conexão identificada."
    elif "conectado" in mensagem_lower:
        return "Sistema conectado com sucesso a um recurso."
    else:
        return "Evento registrado no sistema. Sem categoria definida."

def converter_timestamp(timestamp_str):
    try:
        microssegundos = int(timestamp_str)
        segundos = microssegundos / 1_000_000
        return datetime.utcfromtimestamp(segundos).isoformat() + 'Z'
    except (ValueError, TypeError):
        return datetime.utcnow().isoformat() + 'Z'
