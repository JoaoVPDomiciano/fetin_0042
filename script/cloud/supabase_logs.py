import requests

SUPABASE_URL = "https://epruvcgigotpcptjaqyr.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVwcnV2Y2dpZ290cGNwdGphcXlyIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc0Njk2MzcxMywiZXhwIjoyMDYyNTM5NzEzfQ.zIA2LO93He3kKRYhSv52w0GxoEFV9ILF7-uW196jb50"
SUPABASE_TABELA = "logs"

def enviar_logs_para_supabase(log):
    url = f"{SUPABASE_URL}/rest/v1/{SUPABASE_TABELA}"
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

def limpar_logs_supabase():
    try:
        headers = {
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {SUPABASE_KEY}",
            "Content-Type": "application/json"
        }

        # Busca o ID do 500º log mais recente
        url_select = f"{SUPABASE_URL}/rest/v1/{SUPABASE_TABELA}?select=id&order=id.desc&offset=499&limit=1"
        res = requests.get(url_select, headers=headers)
        res.raise_for_status()
        data = res.json()

        if data:
            limite_id = data[0]['id']

            # Deleta logs com id menor que o limite
            url_delete = f"{SUPABASE_URL}/rest/v1/{SUPABASE_TABELA}?id=lt.{limite_id}"
            del_res = requests.delete(url_delete, headers=headers)
            del_res.raise_for_status()
            print("[OK] Logs antigos removidos da Supabase.")
        else:
            print("[OK] Menos de 500 registros na Supabase.")

    except Exception as e:
        print(f"[ERRO] Falha ao limpar logs da Supabase: {e}")
