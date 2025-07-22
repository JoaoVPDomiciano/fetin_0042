import subprocess
from datetime import datetime
import re

PORT_MAP = {
    # 🌐 Web / Navegação
    80: "Web - HTTP (Navegação não segura)",
    443: "Web - HTTPS (Navegação segura)",
    8080: "Web - Proxy HTTP",
    8443: "Web - HTTPS alternativo",

    # 📧 E-mail
    25: "SMTP - Envio de E-mails",
    110: "POP3 - Recebimento de E-mails (inseguro)",
    143: "IMAP - Acesso remoto a e-mails (inseguro)",
    465: "SMTPS - SMTP Seguro (legacy)",
    587: "SMTP - Envio autenticado (moderno)",
    993: "IMAPS - IMAP Seguro",
    995: "POP3S - POP3 Seguro",

    # 📁 Transferência de Arquivos
    20: "FTP - Dados",
    21: "FTP - Controle",
    22: "SSH / SFTP - Acesso remoto e transferência segura",
    69: "TFTP - Trivial FTP (usado em dispositivos embarcados)",
    989: "FTPS - FTP sobre TLS (dados)",
    990: "FTPS - FTP sobre TLS (controle)",

    # 🔒 Acesso remoto / Administração
    23: "Telnet - Acesso remoto não criptografado",
    3389: "RDP - Área de Trabalho Remota (Windows)",

    # 🕑 Tempo / Sincronização
    123: "NTP - Protocolo de Tempo de Rede",

    # 🎥 Streaming / Mídia
    554: "RTSP - Protocolo de Streaming",
    1755: "MMS - Microsoft Media Services",
    1935: "RTMP - Streaming Flash",
    7070: "RealAudio Streaming",
    8000: "SHOUTcast/Icecast - Rádio/Streaming",
    8554: "RTSP Alternativo",

    # 📡 DNS
    53: "DNS - Resolução de nomes",
    853: "DNS-over-TLS",

    # 🛡️ VPNs
    1194: "OpenVPN",
    500: "IPSec (ISAKMP)",
    1701: "L2TP",
    4500: "IPSec NAT-T",
    1723: "PPTP",
    51820: "WireGuard",

    # 🗂️ Compartilhamento e serviços Microsoft
    135: "DCE/RPC - MS Serviços Remotos",
    137: "NetBIOS - Nome",
    138: "NetBIOS - Datagramas",
    139: "NetBIOS - Sessões",
    445: "SMB - Compartilhamento de Arquivos (Windows)",

    # 🧠 Banco de Dados
    1433: "SQL Server",
    1521: "Oracle DB",
    3306: "MySQL/MariaDB",
    5432: "PostgreSQL",
    27017: "MongoDB",
    6379: "Redis",
    50000: "DB2 (IBM)",

    # ☁️ Serviços em Nuvem / Backend
    2375: "Docker (API não segura)",
    2376: "Docker (API segura)",
    6443: "Kubernetes API",
    4505: "SaltStack Publisher",
    4506: "SaltStack Worker",

    # 🧠 IoT / Mensageria
    1883: "MQTT - Mensageria IoT",
    8883: "MQTTS - MQTT Seguro",
    5683: "CoAP - Protocolo IoT leve",
    4840: "OPC UA - Automação industrial",

    # 💬 Mensageiros e Apps
    5222: "XMPP/Jabber - Chat",
    5228: "Google Play Services",
    3478: "STUN - WebRTC / Chamadas (Zoom, Meet)",
    19302: "Google WebRTC (STUN)",

    # 🕹️ Jogos e plataformas
    25565: "Minecraft",
    27015: "Steam (Valve)",
    5000: "League of Legends (PBE)",
    3074: "Xbox Live / Call of Duty",
    6112: "Blizzard (Diablo, WoW)",
    27960: "Quake/Enemy Territory",

    # 🎛️ Outros / Diversos
    8081: "Painel Web Alternativo",
    9000: "SonarQube / Desenvolvimento",
    9090: "Prometheus / Monitoramento",
    1812: "RADIUS - Autenticação",
    161: "SNMP - Monitoramento de rede",
    514: "Syslog - Log de Sistema",

    # 🚫 Desconhecida
    0: "Porta inválida ou não identificada"
}


def classificar_trafego(interface='eth0', duracao=10):
    try:
        comando = [
            "sudo", "tcpdump", "-i", interface, "-nn", "-t", "-c", "100"
        ]
        resultado = subprocess.run(comando, capture_output=True, text=True, timeout=duracao)

        trafego = []
        linhas = resultado.stdout.splitlines()
        for linha in linhas:
            portas = re.findall(r'\.(\d{1,5})', linha)
            if portas:
                porta = int(portas[-1])
                tipo = PORT_MAP.get(porta, "Outro")
                trafego.append({
                    "timestamp": datetime.now().isoformat(),
                    "porta": porta,
                    "tipo": tipo
                })

        return trafego

    except subprocess.TimeoutExpired:
        print("Timeout na captura de pacotes.")
        return []
    except Exception as e:
        print(f"[ERRO] Falha ao classificar tráfego: {e}")
        return []
