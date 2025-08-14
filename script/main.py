import time
import threading
import requests
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

from monitor.ST_runner import testar_conexao
from monitor.log_collector import coletar_logs
from monitor.traffic_classifier import classificar_trafego

from database.local_ST import criar_tabela_speedTest, salvar_sqlite_speedTest
from database.local_logs import criar_tabela_logs, salvar_sqlite_logs
from database.local_traffic import criar_tabela_trafego, salvar_sqlite_trafego

from cloud.supabase_ST import enviar_para_supabase
from cloud.supabase_logs import enviar_logs_para_supabase
from cloud.supabase_traffic import enviar_trafego_para_supabase

from rotation.data_rotation_logs import clean_logs_data
from rotation.data_rotation_speedtest import clean_speedtest_data
from rotation.data_rotation_trafego import clean_trafego_data

INTERVALO_TESTE = 120
INTERVALO_LOGS = 3000
INTERVALO_TRAF = 6000
LINHAS_LOGS = 100

def verificar_usuario(email, senha):
    url = f"{SUPABASE_URL}/rest/v1/usuarios?email=eq.{email}&senha=eq.{senha}"
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        usuarios = response.json()
        if usuarios:
            horarios = usuarios[0]["horario1"], usuarios[0]["horario2"], usuarios[0]["horario3"]
            return True, horarios
        else:
            return False, None
    else:
        print(f"Erro ao buscar usuário: {response.status_code}")
        return False, None

def rotina_speedtest(horarios):
    while True:
        resultado = testar_conexao()
        salvar_sqlite_speedTest(resultado)
        enviar_para_supabase(resultado)
        print("Teste de velocidade concluído e enviado.")

        clean_speedtest_data()
        time.sleep(120)

def rotina_logs(horarios):
    while True:
        logs = coletar_logs(100)
        for log in logs:
            salvar_sqlite_logs(log)
            enviar_logs_para_supabase(log)
        print(f"{len(logs)} logs coletados e enviados.")

        clean_logs_data()
        time.sleep(3000)

def rotina_trafego(horarios):
    while True:
        pacotes = classificar_trafego()
        for pacote in pacotes:
            salvar_sqlite_trafego(pacote)
            enviar_trafego_para_supabase(pacote)
        print(f" {len(pacotes)} pacotes classificados e enviados.")

        clean_trafego_data()
        time.sleep(6000)

def main():
    email = input("Digite seu e-mail: ")
    senha = input("Digite sua senha: ")

    autenticado, horarios = verificar_usuario(email, senha)

    if autenticado:
        print("Usuário autenticado com sucesso!")
        print(f"Horários cadastrados: {horarios}")

        criar_tabela_speedTest()
        criar_tabela_logs()
        criar_tabela_trafego()

        t1 = threading.Thread(target=rotina_speedtest, args=(horarios,))
        t2 = threading.Thread(target=rotina_logs, args=(horarios,))
        t3 = threading.Thread(target=rotina_trafego, args=(horarios,))

        t1.start()
        t2.start()
        t3.start()

        t1.join()
        t2.join()
        t3.join()

    else:
        print("Usuário ou senha incorretos. Tente novamente.")

if __name__ == "__main__":
    main()
