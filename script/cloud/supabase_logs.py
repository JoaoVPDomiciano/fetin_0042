import requests

SUPABASE_URL = "https://epruvcgigotpcptjaqyr.supabase.co"
SUPABASE_KEY = "your_supabase_key_here"

def enviar_logs_para_supabase(log):
    url = f"{SUPABASE_URL}/rest/v1/logs"
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=minimal"
    }

    check_url = f"{SUPABASE_URL}/rest/v1/logs?select=id"
    response = requests.get(check_url, headers=headers)
    if response.status_code == 200:
        registros = response.json()
        if len(registros) >= 500:
            delete_url = f"{SUPABASE_URL}/rest/v1/logs?select=id&order=timestamp.asc&limit=500"
            delete_response = requests.delete(delete_url, headers=headers)
            if delete_response.status_code == 204:
                print("🧹 Dados antigos apagados com sucesso dos Logs no Supabase.")
            else:
                print(f"⚠️ Erro ao apagar dados antigos: {delete_response.text}")

    response = requests.post(url, headers=headers, json=log)
    if response.status_code in [200, 201]:
        print("☁️ Log enviado com sucesso para Supabase!")
    else:
        print(f"⚠️ Erro ao enviar log: {response.status_code}\n{response.text}")