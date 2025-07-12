import os
import requests
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

def enviar_logs_para_supabase(log):
    url = f"{SUPABASE_URL}/rest/v1/logs"
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=minimal"
    }

    dados_para_enviar = {
        "timestamp": log.get("timestamp"),
        "mensagem": log.get("mensagem"),
        "nivel": log.get("nivel"),
        "origem": log.get("origem"),
        "evento_id": log.get("evento_id")
    }

    response = requests.post(url, headers=headers, json=dados_para_enviar)
    if response.status_code in [200, 201]:
        print("Log enviado com sucesso para Supabase!")

    else:
        print(f"Erro ao enviar log: {response.status_code}\n{response.text}")