"""
Envio dos dados para a nuvem.
"""

import requests

SUPABASE_URL = "https://epruvcgigotpcptjaqyr.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVwcnV2Y2dpZ290cGNwdGphcXlyIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc0Njk2MzcxMywiZXhwIjoyMDYyNTM5NzEzfQ.zIA2LO93He3kKRYhSv52w0GxoEFV9ILF7-uW196jb50"
def enviar_para_supabase(dados):
    url = f"{SUPABASE_URL}/rest/v1/speedtest"
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=minimal"
    }

    response = requests.post(url, headers=headers, json=dados)
    if response.status_code in [200, 201]:
        print("☁️ Dados enviados com sucesso para Supabase!")
    else:
        print(f"⚠️ Falha ao enviar dados: {response.status_code}\n{response.text}")
