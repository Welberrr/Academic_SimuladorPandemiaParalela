import random
import multiprocessing
import time
import numpy as np
import matplotlib.pyplot as plt

def processar_infectados(args):
    populacao, infectados_ids, taxa_transmissao, taxa_recuperacao, contatos_por_dia = args
    alteracoes = {}

    for i in infectados_ids:
        for _ in range(contatos_por_dia):
            alvo = random.randint(0, len(populacao) - 1)
            if populacao[alvo] == 'S' and random.random() < taxa_transmissao:
                alteracoes[alvo] = 'I'
        if random.random() < taxa_recuperacao:
            alteracoes[i] = 'R'
    
    return alteracoes

def simular_epidemia_baseado_em_agentes(populacao_total, vacinados, dias, taxa_transmissao=0.05, taxa_recuperacao=0.01, contatos_por_dia=10, plano_vacinacao=None):
    populacao = np.full(populacao_total, 'S', dtype='<U1')
    populacao[:vacinados] = 'R'
    populacao[vacinados:vacinados + 10] = 'I'
    np.random.shuffle(populacao)

    infectados_hist, recuperados_hist, suscetiveis_hist = [], [], []
    n_processos = multiprocessing.cpu_count()

    for dia in range(dias):
        # Aplicar vacinação se houver plano
        if plano_vacinacao and dia in plano_vacinacao:
            novos_vacinados = plano_vacinacao[dia]
            vacinados_hoje = 0
            for i in range(len(populacao)):
                if populacao[i] == 'S':
                    populacao[i] = 'R'
                    vacinados_hoje += 1
                    if vacinados_hoje >= novos_vacinados:
                        break
            print(f"[Dia {dia+1}] {vacinados_hoje} pessoas vacinadas.")

        infectados_ids = np.where(populacao == 'I')[0].tolist()
        if not infectados_ids:
            print(f"[Dia {dia+1}] Epidemia acabou.")
            break

        chunk_size = max(1, len(infectados_ids) // n_processos)
        tarefas = [
            (populacao.copy(), infectados_ids[i:i + chunk_size], taxa_transmissao, taxa_recuperacao, contatos_por_dia)
            for i in range(0, len(infectados_ids), chunk_size)
        ]

        with multiprocessing.Pool(processes=n_processos) as pool:
            resultados = pool.map(processar_infectados, tarefas)

        for resultado in resultados:
            for idx, novo_estado in resultado.items():
                populacao[idx] = novo_estado

        # Estatísticas do dia
        infectados = np.count_nonzero(populacao == 'I')
        recuperados = np.count_nonzero(populacao == 'R')
        suscetiveis = np.count_nonzero(populacao == 'S')

        infectados_hist.append(infectados)
        recuperados_hist.append(recuperados)
        suscetiveis_hist.append(suscetiveis)

        print(f"[Dia {dia+1}] S: {suscetiveis} | I: {infectados} | R: {recuperados}")

    return suscetiveis_hist, infectados_hist, recuperados_hist

def plotar_resultados(S, I, R):
    plt.figure(figsize=(10, 6))
    plt.plot(S, label="Suscetíveis (S)")
    plt.plot(I, label="Infectados (I)")
    plt.plot(R, label="Recuperados (R)")
    plt.title("Evolução da Epidemia (Valores Absolutos)")
    plt.xlabel("Dias")
    plt.ylabel("Número de Pessoas")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def plotar_grafico_percentual(S_hist, I_hist, R_hist):
    dias = list(range(len(S_hist)))
    total_pop = np.array(S_hist) + np.array(I_hist) + np.array(R_hist)

    S_pct = (np.array(S_hist) / total_pop) * 100
    I_pct = (np.array(I_hist) / total_pop) * 100
    R_pct = (np.array(R_hist) / total_pop) * 100

    plt.figure(figsize=(10, 6))
    plt.plot(dias, S_pct, label="Suscetíveis (%)")
    plt.plot(dias, I_pct, label="Infectados (%)")
    plt.plot(dias, R_pct, label="Recuperados (%)")
    plt.title("Proporção de Estados ao Longo do Tempo (%)")
    plt.xlabel("Dias")
    plt.ylabel("Percentual (%)")
    plt.ylim(0, 100)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def main():
    print("=== Simulação de Epidemia com Modelo Baseado em Agentes ===")

    while True:
        try:
            populacao_total = int(input("Digite a população total: "))
            vacinados = int(input("Digite o número de vacinados no início: "))
            dias = int(input("Digite o número de dias da simulação: "))
            if populacao_total <= 0 or vacinados < 0 or vacinados > populacao_total or dias <= 0:
                raise ValueError
            break
        except ValueError:
            print("Entradas inválidas. Por favor, insira valores inteiros positivos e consistentes.")

    plano_vacinacao = {}
    usar_vacinacao_tardia = input("Deseja aplicar vacinação em massa após alguns dias? (s/n): ").strip().lower() == 's'
    if usar_vacinacao_tardia:
        while True:
            try:
                qtd_vac_dias = int(input("Quantos dias diferentes terão vacinação em massa? "))
                for _ in range(qtd_vac_dias):
                    dia = int(input("Digite o dia (ex: 7): "))
                    qtd = int(input(f"Quantas pessoas vacinar no dia {dia}? "))
                    plano_vacinacao[dia] = qtd
                break
            except ValueError:
                print("Por favor, digite números válidos.")

    print("\nIniciando simulação...\n")
    t0 = time.time()

    S_hist, I_hist, R_hist = simular_epidemia_baseado_em_agentes(
        populacao_total,
        vacinados,
        dias,
        taxa_transmissao=0.05,
        taxa_recuperacao=0.01,
        contatos_por_dia=10,
        plano_vacinacao=plano_vacinacao
    )

    duracao = time.time() - t0

    print("\n=== Resultados Finais ===")
    print(f"Total de dias simulados: {len(I_hist)}")
    print(f"Pico de infectados: {max(I_hist)}")
    print(f"Total de recuperados: {R_hist[-1]}")
    print(f"Tempo total de execução: {duracao:.2f} segundos ({duracao / 60:.2f} minutos)")

    plotar_resultados(S_hist, I_hist, R_hist)
    plotar_grafico_percentual(S_hist, I_hist, R_hist)

if __name__ == "__main__":
    multiprocessing.freeze_support()
    main()
