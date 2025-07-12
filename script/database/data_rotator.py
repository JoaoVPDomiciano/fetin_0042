import requests

SUPABASE_URL = "https://epruvcgigotpcptjaqyr.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVwcnV2Y2dpZ290cGNwdGphcXlyIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc0Njk2MzcxMywiZXhwIjoyMDYyNTM5NzEzfQ.zIA2LO93He3kKRYhSv52w0GxoEFV9ILF7-uW196jb50"

HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

def clean_sqlite_table(conn, table_name):
    cursor = conn.cursor()
    cursor.execute(f'''
        DELETE FROM {table_name}
        WHERE id NOT IN (
            SELECT id FROM {table_name}
            ORDER BY id DESC
            LIMIT 100
        )
    ''')
    conn.commit()

def clean_supabase_table(table_name):
    # Passo 1: Buscar os 100 IDs mais recentes
    url_select = f"{SUPABASE_URL}/rest/v1/{table_name}?select=id&order=id.desc&limit=100"
    response = requests.get(url_select, headers=HEADERS)

    if response.status_code == 200:
        ids = response.json()
        if not ids:
            print("📭 Nenhum dado encontrado no Supabase.")
            return

        ids_to_keep = [row["id"] for row in ids]
        min_id = min(ids_to_keep)

        # Passo 2: Deletar todos com id < min_id
        url_delete = f"{SUPABASE_URL}/rest/v1/{table_name}?id=lt.{min_id}"
        delete_headers = {
            **HEADERS,
            "Prefer": "return=minimal"
        }
        del_response = requests.delete(url_delete, headers=delete_headers)
        if del_response.status_code in [200, 204]:
            print("🧹 Supabase limpo com sucesso.")
        else:
            print(f"⚠️ Erro ao deletar: {del_response.status_code} - {del_response.text}")
    else:
        print(f"⚠️ Falha na busca de dados: {response.status_code} - {response.text}")
