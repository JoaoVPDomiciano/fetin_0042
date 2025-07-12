import os
import requests
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

def enviar_trafego_para_supabase(pacotes):
    url = f"{SUPABASE_URL}/rest/v1/trafego"
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=minimal"
    }

    response = requests.post(url, headers=headers, json=pacotes)
    if response.status_code in [200, 201]:
        print(f"Erro ao enviar tráfego: {response.status_code} - {response.text}")
    else:
        print(f"Falha ao enviar dados: {response.status_code}\n{response.text}")
