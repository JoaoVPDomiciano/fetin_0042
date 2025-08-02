import subprocess
from datetime import datetime
import re

PORT_MAP_EXTENSO = {
    # 🌐 Web
    80: "HTTP - Navegação web padrão (insegura)",
    443: "HTTPS - Navegação segura (SSL/TLS)",
    8080: "HTTP alternativo / Proxy",
    8443: "HTTPS alternativo",
    8880: "HTTP proxy alternativo (Cloudflare, cPanel)",

    # 📧 E-mail
    25: "SMTP - Envio de e-mails (inseguro)",
    110: "POP3 - Recebimento de e-mails (inseguro)",
    143: "IMAP - Acesso a e-mails (inseguro)",
    465: "SMTPS - SMTP seguro (SSL)",
    587: "SMTP autenticado (STARTTLS)",
    993: "IMAPS - IMAP seguro",
    995: "POP3S - POP3 seguro",

    # 📁 Transferência de arquivos
    20: "FTP - Dados",
    21: "FTP - Controle",
    22: "SSH/SFTP - Acesso remoto seguro",
    989: "FTPS - Dados seguros",
    990: "FTPS - Controle seguro",
    69: "TFTP - Trivial File Transfer Protocol",

    # 🔒 Acesso remoto / Administração
    23: "Telnet - Acesso remoto não seguro",
    3389: "RDP - Área de trabalho remota",
    2222: "SSH alternativo (frequente em embedded)",
    5800: "VNC via HTTP",
    5900: "VNC - Controle remoto de desktop",

    # 📡 DNS
    53: "DNS - Resolução de nomes",
    853: "DNS-over-TLS",
    5353: "mDNS - Multicast DNS",
    5355: "LLMNR - Link-Local Multicast Name Resolution",

    # 🕑 Tempo
    123: "NTP - Protocolo de sincronização de tempo",

    # 🛡️ VPNs
    500: "IPSec - ISAKMP",
    1701: "L2TP",
    1723: "PPTP",
    4500: "IPSec NAT-T",
    1194: "OpenVPN (UDP)",
    51820: "WireGuard VPN",
    443: "VPNs stealth via TLS (OpenVPN, etc.)",

    # 🧠 Banco de dados
    1433: "SQL Server",
    3306: "MySQL/MariaDB",
    5432: "PostgreSQL",
    1521: "Oracle DB",
    27017: "MongoDB",
    6379: "Redis",
    9042: "Cassandra",
    50000: "IBM DB2",

    # ☁️ Serviços em nuvem
    2375: "Docker - API não segura",
    2376: "Docker - API segura",
    6443: "Kubernetes API",
    10250: "Kubelet API",
    8500: "Consul - Service discovery",
    8200: "Vault - Gerenciamento de segredos",
    5050: "Mesos Master",
    9090: "Prometheus",
    9093: "Alertmanager",
    3000: "Grafana",
    5601: "Kibana",

    # 🧠 IoT / Automação
    1883: "MQTT - Protocolo de mensagens para IoT",
    8883: "MQTT seguro (TLS)",
    5683: "CoAP - IoT leve",
    4840: "OPC UA - Indústria/automação",
    49152: "UPnP - Plug and play (IoT, câmeras)",
    9999: "TP-Link Smart Devices",

    # 💬 Mensagens / VoIP
    5060: "SIP - Início de chamadas VoIP (UDP)",
    5061: "SIP seguro (TLS)",
    3478: "STUN/TURN - WebRTC / Zoom / Meet",
    19302: "STUN - Google",
    5222: "XMPP - Chat / Mensagens",
    5228: "Google Play Services",
    1863: "MSN Messenger (legacy)",

    # 🎮 Jogos online
    25565: "Minecraft",
    27015: "Steam - Jogos Valve",
    5000: "League of Legends (PBE)",
    3074: "Xbox Live / Call of Duty",
    6112: "Blizzard - Diablo, WoW",
    28960: "Call of Duty: Modern Warfare",
    27960: "Quake / Enemy Territory",
    3659: "EA Games (FIFA, BF)",
    5005: "Rocket League",

    # 🖥️ Serviços Windows / MS
    135: "DCE/RPC - Serviços MS",
    137: "NetBIOS - Nome",
    138: "NetBIOS - Datagramas",
    139: "NetBIOS - Sessão",
    445: "SMB - Compartilhamento de arquivos",

    # 📈 Monitoramento
    161: "SNMP - Monitoramento de rede",
    162: "SNMP Trap",
    514: "Syslog",
    2003: "Graphite - Métricas",
    8125: "StatsD",
    8126: "DogStatsD",
    19999: "Netdata",

    # 🎛️ Outros serviços
    3000: "Painel Web (Node.js / Grafana)",
    8081: "Web Interface Alternativa",
    9000: "SonarQube / Dev",
    10000: "Webmin - Administração web",
    20000: "Usermin - Painel de usuário",
    12345: "NetBus - Backdoor (legacy)",
    31337: "Elite - Histórico de backdoors",
    6667: "IRC - Internet Relay Chat",

    # 🚫 Desconhecida
    0: "Porta inválida ou desconhecida"
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
