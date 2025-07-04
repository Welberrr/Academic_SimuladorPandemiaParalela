# 🧬 SIMULAÇÃO DE PANDEMIA BASEADO EM AGENTES

Um sistema de simulação epidemiológica que utiliza processamento paralelo para modelar a disseminação de uma pandemia em uma população massiva, com suporte a vacinação e análise temporal da infecção.

--------------------------------------------------------------------------------

# 📋 Introdução
Este projeto implementa uma simulação baseada em agentes para modelar a propagação de uma doença infecciosa em larga escala. O objetivo principal é comparar a eficiência entre versões serial e paralela da simulação, demonstrando como técnicas de paralelismo podem melhorar significativamente o tempo de execução em cenários computacionalmente intensivos.

# 🎯 Descrição do Problema
Modelagens realistas de epidemias exigem a simulação de milhões de indivíduos, o que leva a tempos de execução elevados em abordagens sequenciais. Os principais desafios enfrentados foram:

🧠 Alta complexidade computacional: grande número de agentes interagindo diariamente.

🕒 Desempenho: necessidade de reduzir o tempo de simulação.

⚖️ Escalabilidade: capacidade de expandir para diferentes quantidades de núcleos de CPU.

💉 Eventos dinâmicos: como vacinação em massa em dias específicos.

# 🛠️ Descrição da Solução
🔄 Versão Serial
Simulação sequencial que processa interações entre agentes de forma linear, sendo usada como referência base para análise de performance.

🧵 Versão Paralela
Implementada com multiprocessing, a população é compartilhada via RawArray e os agentes infectados são divididos entre processos:

Distribuição balanceada das tarefas

Redução drástica no tempo de execução

Suporte para 2, 4, 8 e 16 processos simultâneos

# ⚙️ Configurações da Simulação
👥 População: 25.000.000

😷 Infectados Iniciais: 2.500.000

📆 Dias de Simulação: 45

💉 Vacinação em Massa: 500.000 pessoas no dia 1

📌 Taxa de Transmissão: 5%

📌 Taxa de Recuperação: 1%

🔁 Contatos por dia por infectado: 10

--------------------------------------------------------------------------------

# 📊 Tabela de Performance

![image](https://github.com/user-attachments/assets/9ed45fdd-25c8-4306-80c9-7a8ab8df43a1)

# 📉 Speedup vs Eficiencia

![image](https://github.com/user-attachments/assets/02ab1b0c-b2c3-4316-8730-b7370bf64d45)

📉 # Eficiencia

![image](https://github.com/user-attachments/assets/cd16bbf6-cf1a-4641-af5e-e4b0a0e14224)

# 📉 Speedup

![image](https://github.com/user-attachments/assets/4d3aa1fb-d5b9-4ec9-81ec-dd0e9ca2845c)

--------------------------------------------------------------------------------

# ✅ Conclusão
A simulação paralela apresentou um desempenho significativamente superior à versão serial:

# Principais Conquistas
🚀 Speedup de até 10.5x com 16 processos

⏱️ Tempo de execução reduzido de 676s para 64s

⚙️ Eficiência > 84% até 8 threads

🔄 Manutenção da dinâmica epidemiológica mesmo com paralelismo

# Impacto
📉 Redução massiva no tempo de execução

🧪 Possibilidade de simular cenários mais complexos

🧩 Estrutura modular e escalável

# Limitações Observadas
📉 Eficiência reduzida com mais de 8 processos devido ao overhead

🧠 Custo de sincronização e compartilhamento de memória entre processos

--------------------------------------------------------------------------------

# 💻 Execução
Instale as dependências:

bash
Copiar
Editar
pip install -r requirements.txt

Execute a simulação:

bash
Copiar
Editar
# Serial
python simulacao_serial.py

## Paralelo (ex: com 8 processos)
python simulacao_paralela.py

# Dados de entrada:

População: 25000000

Infectados: 2500000 

Dias de simulação: 45

Numero de processos: (feito com todos: 2, 4, 8 e 16 e apenas 1 na versao serial)

Vacinação em massa: s

dias de vacinação em massa: 1

total de vacinados: 500000

--------------------------------------------------------------------------------

# 👥 Autor
Welber Henrique
