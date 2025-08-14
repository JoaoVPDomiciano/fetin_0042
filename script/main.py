import os
import time
import threading
import requests
from datetime import datetime, time as time_obj
from urllib.parse import quote
from dotenv import load_dotenv

# --- Carregar variáveis de ambiente ---
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# --- Imports de módulos locais ---
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


# --- Configurações ---
INTERVALO_LOGS = 3000
INTERVALO_TRAF = 6000
TOLERANCIA_SEGUNDOS = 30


# --- Funções utilitárias ---
def verificar_usuario(email):
    """
    Consulta o usuário no Supabase e retorna os horários configurados.
    """
    email_encoded = quote(email)
    url = f"{SUPABASE_URL}/rest/v1/cadastro?email=eq.{email_encoded}&limit=1"
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        usuarios = response.json()
        if usuarios:
            return True, (
                usuarios[0]["primeiro"],
                usuarios[0]["segundo"],
                usuarios[0]["terceiro"]
            )
        return False, None
    else:
        print(f"URL chamada: {url}")
        print(f"Erro ao buscar usuário: {response.status_code} - {response.text}")
        return False, None


def parse_horarios(horarios_str):
    """
    Converte lista de horários em string para objetos datetime.time,
    ignorando inválidos.
    """
    horarios_time = []
    for h in horarios_str:
        try:
            horarios_time.append(datetime.strptime(h, "%H:%M:%S").time())
        except ValueError:
            print(f"⚠ Horário inválido ignorado: {h}")
    return horarios_time


def dentro_da_tolerancia(agora, horarios):
    """
    Verifica se o horário atual está dentro da tolerância de segundos
    para algum dos horários configurados.
    """
    agora_dt = datetime.combine(datetime.today(), agora)
    for h in horarios:
        alvo_dt = datetime.combine(datetime.today(), h)
        if abs((agora_dt - alvo_dt).total_seconds()) <= TOLERANCIA_SEGUNDOS:
            return True
    return False


# --- Rotinas principais ---
def rotina_speedtest(horarios):
    while True:
        agora = datetime.now().time().replace(microsecond=0)

        if dentro_da_tolerancia(agora, horarios):
            print(f"⏳ Executando SpeedTest às {agora}...")
            resultado = testar_conexao()
            salvar_sqlite_speedTest(resultado)
            enviar_para_supabase(resultado)
            print("✅ Teste de velocidade concluído e enviado.")
            clean_speedtest_data()
            time.sleep(60)  # Evita execução múltipla no mesmo minuto
        else:
            time.sleep(20)  # Verificação periódica


def rotina_logs():
    while True:
        logs = coletar_logs(100)
        for log in logs:
            salvar_sqlite_logs(log)
            enviar_logs_para_supabase(log)
        print(f"{len(logs)} logs coletados e enviados.")
        clean_logs_data()
        time.sleep(INTERVALO_LOGS)


def rotina_trafego():
    while True:
        pacotes = classificar_trafego()
        for pacote in pacotes:
            salvar_sqlite_trafego(pacote)
            enviar_trafego_para_supabase(pacote)
        print(f"{len(pacotes)} pacotes classificados e enviados.")
        clean_trafego_data()
        time.sleep(INTERVALO_TRAF)


# --- Função principal ---
def main():
    email = input("Digite seu e-mail: ")
    autenticado, horarios_str = verificar_usuario(email)

    if not autenticado:
        print("Usuário não encontrado. Tente novamente.")
        return

    print("Usuário autenticado com sucesso!")
    print(f"Horários cadastrados: {horarios_str}")

    horarios_time = parse_horarios(horarios_str)
    print(f"Horários configurados para SpeedTest: {horarios_time}")

    # Criar tabelas locais
    criar_tabela_speedTest()
    criar_tabela_logs()
    criar_tabela_trafego()

    # Iniciar threads
    t1 = threading.Thread(target=rotina_speedtest, args=(horarios_time,))
    t2 = threading.Thread(target=rotina_logs)
    t3 = threading.Thread(target=rotina_trafego)

    t1.start()
    t2.start()
    t3.start()

    t1.join()
    t2.join()
    t3.join()


if __name__ == "__main__":
    main()
