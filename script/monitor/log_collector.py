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
                mensagem_original = log.get("MESSAGE", "Sem detalhes disponíveis no momento.")
                mensagem_humanizada = humanizar_mensagem(mensagem_original.lower())

                log_entry = {
                    "timestamp": converter_timestamp(log.get("__REALTIME_TIMESTAMP")),
                    "mensagem": mensagem_humanizada
                }

                if any(palavra in mensagem_original.lower() for palavra in PALAVRAS_CHAVE):
                    logs_filtrados.append(log_entry)

            except json.JSONDecodeError:
                continue

        return logs_filtrados

    except Exception as e:
        print(f"[ERRO] Ocorreu um problema ao tentar coletar os registros do sistema. Motivo: {e}")
        return []

def humanizar_mensagem(mensagem):
    if "dns" in mensagem:
        return "Problema ao encontrar o endereço de um site. Verifique sua conexão com a internet."
    elif "timeout" in mensagem:
        return "O sistema demorou para responder. Isso pode indicar lentidão ou falha na conexão."
    elif "fail" in mensagem or "falha" in mensagem:
        return "Ocorreu uma falha no sistema. Verifique se todos os serviços estão funcionando corretamente."
    elif "erro" in mensagem:
        return "Um erro foi detectado. É recomendável verificar os detalhes técnicos ou reiniciar o sistema."
    elif "restart" in mensagem:
        return "Um componente do sistema foi reiniciado automaticamente."
    elif "dhcp" in mensagem:
        return "Configuração automática de rede detectada. Pode estar tentando obter um novo IP."
    elif "ip" in mensagem:
        return "Alteração ou problema com o endereço IP."
    elif "driver" in mensagem:
        return "Um driver do sistema pode estar com problema. Verifique os dispositivos conectados."
    elif "desconectado" in mensagem:
        return "O sistema perdeu a conexão com a rede ou dispositivo."
    elif "conexão" in mensagem:
        return "Alteração ou problema na conexão detectado."
    elif "conectado" in mensagem:
        return "O sistema foi conectado com sucesso à rede ou dispositivo."
    else:
        return "Atividade registrada no sistema. Para mais detalhes, consulte um técnico."

def converter_timestamp(timestamp_str):
    try:
        microssegundos = int(timestamp_str)
        segundos = microssegundos / 1_000_000
        return datetime.utcfromtimestamp(segundos).isoformat() + 'Z'
    except (ValueError, TypeError):
        return datetime.utcnow().isoformat() + 'Z'