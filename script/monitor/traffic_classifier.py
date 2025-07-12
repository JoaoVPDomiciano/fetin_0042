import subprocess
from datetime import datetime
import re

PORT_MAP = {
    80: "Web (HTTP)",
    443: "Web (HTTPS)",
    53: "DNS",
    25: "Email (SMTP)",
    110: "Email (POP3)",
    21: "FTP",
    22: "SSH",
    1935: "Streaming (RTMP)",
    554: "Streaming (RTSP)",
    123: "NTP",
    993: "Email (IMAPS)",
    995: "Email (POP3S)",
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
