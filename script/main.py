import time
import threading

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

INTERVALO_TESTE = 60        # Segundos entre testes de velocidade
INTERVALO_LOGS = 30        # Segundos entre capturas de logs
INTERVALO_TRAF = 15         # Segundos entre capturas
LINHAS_LOGS = 10             # Quantidade de logs recentes a coletar por vez

def rotina_speedtest():
    while True:
        resultado = testar_conexao()
        salvar_sqlite_speedTest(resultado)
        enviar_para_supabase(resultado)
        print("Teste de velocidade concluído e enviado.")

        clean_speedtest_data()
        time.sleep(INTERVALO_TESTE)

def rotina_logs():
    while True:
        logs = coletar_logs(LINHAS_LOGS)
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
        print(f" {len(pacotes)} pacotes classificados e enviados.")

        clean_trafego_data()
        time.sleep(INTERVALO_TRAF)

def main():
    criar_tabela_speedTest()
    criar_tabela_logs()
    criar_tabela_trafego()

    t1 = threading.Thread(target=rotina_speedtest)
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