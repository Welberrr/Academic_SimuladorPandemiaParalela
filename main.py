import random
import multiprocessing
from multiprocessing import RawArray
import time
import numpy as np
import matplotlib.pyplot as plt

# Estados
SUSCETIVEL = 0
INFECTADO = 1
RECUPERADO = 2

# Variáveis globais para multiprocessing
array_compartilhado = None
shape = None

def inicializar_pool(array, array_shape):
    global array_compartilhado, shape
    array_compartilhado = array
    shape = array_shape

def processar_infectados(infectados_ids):
    global array_compartilhado, shape
    populacao = np.frombuffer(array_compartilhado, dtype='i1').reshape(shape)
    alteracoes = {}

    for i in infectados_ids:
        for _ in range(10):  # contatos_por_dia
            alvo = random.randint(0, len(populacao) - 1)
            if populacao[alvo] == 0 and random.random() < 0.05:
                alteracoes[alvo] = 1
        if random.random() < 0.01:
            alteracoes[i] = 2

    return alteracoes

def simular_epidemia_baseado_em_agentes(populacao_total, vacinados, dias,
                                        taxa_transmissao=0.05, taxa_recuperacao=0.01,
                                        contatos_por_dia=10, plano_vacinacao=None,
                                        n_processos=4):
    global array_compartilhado, shape

    populacao = np.zeros(populacao_total, dtype=np.int8)
    populacao[:vacinados] = 2  # Recuperado
    populacao[vacinados:vacinados + 10] = 1  # Infectado
    np.random.shuffle(populacao)

    array_compartilhado = multiprocessing.RawArray('b', populacao.tobytes())
    shape = populacao.shape

    infectados_hist, recuperados_hist, suscetiveis_hist = [], [], []

    with multiprocessing.Pool(
        processes=n_processos,
        initializer=inicializar_pool,
        initargs=(array_compartilhado, shape)
    ) as pool:

        for dia in range(dias):
            pop_np = np.frombuffer(array_compartilhado, dtype=np.int8).reshape(shape)

            if plano_vacinacao and dia in plano_vacinacao:
                novos_vacinados = plano_vacinacao[dia]
                vacinados_hoje = 0
                for i in range(len(pop_np)):
                    if pop_np[i] == 0:
                        pop_np[i] = 2
                        vacinados_hoje += 1
                        if vacinados_hoje >= novos_vacinados:
                            break
                print(f"[Dia {dia + 1}] {vacinados_hoje} pessoas vacinadas.")

            infectados_ids = np.where(pop_np == 1)[0].tolist()
            if not infectados_ids:
                print(f"[Dia {dia + 1}] Epidemia acabou.")
                break

            # Distribuir infectados igualmente entre os processos
            tarefas = [[] for _ in range(n_processos)]
            for i, id_infectado in enumerate(infectados_ids):
                tarefas[i % n_processos].append(id_infectado)

            resultados = pool.map(processar_infectados, tarefas)

            for resultado in resultados:
                for idx, novo_estado in resultado.items():
                    pop_np[idx] = novo_estado

            infectados = np.count_nonzero(pop_np == 1)
            recuperados = np.count_nonzero(pop_np == 2)
            suscetiveis = np.count_nonzero(pop_np == 0)

            infectados_hist.append(infectados)
            recuperados_hist.append(recuperados)
            suscetiveis_hist.append(suscetiveis)

            print(f"[Dia {dia + 1}] S: {suscetiveis} | I: {infectados} | R: {recuperados}")

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

    while True:
        try:
            n_processos = int(input("Digite o número de processos (2, 4, 8 ou 16): "))
            if n_processos not in [2, 4, 8, 16]:
                raise ValueError
            break
        except ValueError:
            print("Valor inválido. Digite um dos valores permitidos: 2, 4, 8 ou 16.")

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
        plano_vacinacao=plano_vacinacao,
        n_processos=n_processos
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
