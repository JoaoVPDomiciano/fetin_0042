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
                mensagem_original = log.get("MESSAGE", "").lower()

                if any(palavra in mensagem_original for palavra in PALAVRAS_CHAVE):
                    log_entry = {
                        "timestamp": converter_timestamp(log.get("__REALTIME_TIMESTAMP")),
                        "mensagem_original": log.get("MESSAGE", "Sem detalhes disponíveis."),
                        "explicacao": humanizar_mensagem(mensagem_original),
                        "nivel": mapear_nivel(log.get("PRIORITY")),
                        "origem": log.get("SYSLOG_IDENTIFIER", "Desconhecida"),
                        "evento_id": log.get("MESSAGE_ID", "Sem ID"),
                        "pid": log.get("_PID", "Desconhecido")
                    }

                    logs_filtrados.append(log_entry)

            except json.JSONDecodeError:
                continue

        return logs_filtrados

    except Exception as e:
        print(f"[ERRO] Ocorreu um problema ao tentar coletar os registros do sistema. Motivo: {e}")
        return []

def humanizar_mensagem(mensagem):
    if "dns" in mensagem:
        return "Não foi possível resolver o endereço de um site. Isso pode indicar problemas com os servidores DNS."
    elif "timeout" in mensagem:
        return "A operação demorou demais para responder. Pode estar relacionada à lentidão da internet ou falha do serviço."
    elif "fail" in mensagem or "falha" in mensagem:
        return "Uma falha ocorreu no sistema ou serviço. Isso pode prejudicar a funcionalidade esperada."
    elif "erro" in mensagem:
        return "Um erro foi registrado no sistema. Verifique se algum componente está com problemas."
    elif "restart" in mensagem:
        return "Um serviço foi reiniciado automaticamente. Isso pode ser uma tentativa de recuperação após falha."
    elif "dhcp" in mensagem:
        return "O sistema tentou obter um IP automaticamente via DHCP."
    elif "ip" in mensagem:
        return "Mudança ou falha relacionada ao endereço IP."
    elif "driver" in mensagem:
        return "Ocorreu uma falha ou alteração com um driver. Isso pode afetar periféricos ou hardware."
    elif "desconectado" in mensagem:
        return "Houve uma desconexão de rede ou dispositivo."
    elif "conexão" in mensagem:
        return "Foi detectado um evento de conexão ou tentativa de conexão."
    elif "conectado" in mensagem:
        return "O sistema estabeleceu uma conexão com sucesso."
    else:
        return "Evento do sistema registrado. Verifique os detalhes técnicos para mais informações."

def converter_timestamp(timestamp_str):
    try:
        microssegundos = int(timestamp_str)
        segundos = microssegundos / 1_000_000
        return datetime.utcfromtimestamp(segundos).isoformat() + 'Z'
    except (ValueError, TypeError):
        return datetime.utcnow().isoformat() + 'Z'

def mapear_nivel(prioridade):
    mapa = {
        "0": "Emergência",
        "1": "Alerta",
        "2": "Crítico",
        "3": "Erro",
        "4": "Aviso",
        "5": "Notificação",
        "6": "Informação",
        "7": "Depuração"
    }
    return mapa.get(str(prioridade), "Desconhecido")
