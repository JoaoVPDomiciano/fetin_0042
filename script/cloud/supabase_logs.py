import requests

SUPABASE_URL = "https://epruvcgigotpcptjaqyr.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVwcnV2Y2dpZ290cGNwdGphcXlyIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc0Njk2MzcxMywiZXhwIjoyMDYyNTM5NzEzfQ.zIA2LO93He3kKRYhSv52w0GxoEFV9ILF7-uW196jb50"

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
        print("☁️ Log enviado com sucesso para Supabase!")
    else:
        print(f"⚠️ Erro ao enviar log: {response.status_code}\n{response.text}")