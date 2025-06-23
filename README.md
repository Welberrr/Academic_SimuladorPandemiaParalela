# Academic-SimuladorPandemiaParalela
Projeto integrador da disciplina de computação paralela - Faculdade

Dados de entrada:

25000000
2500000
45
s
1
40
500000

--------------------------------------------------------------------------------
# Resultados
Serial

![image](https://github.com/user-attachments/assets/e1f7f9dc-1732-46b0-93ea-3406903b117e)

![image](https://github.com/user-attachments/assets/5d3a7ca3-3789-4f41-ab97-23c8ad125a6c)


=== Resultados Finais ===
Total de dias simulados: 45
Pico de infectados: 18454424
Total de recuperados: 4083977
Tempo total de execução: 676.51 segundos (11.28 minutos)


2 threads: 

![image](https://github.com/user-attachments/assets/f237f229-b75c-406a-88bb-d04cfb7a6f86)

![image](https://github.com/user-attachments/assets/bcfafebe-e208-47a7-b2de-8356ac34db70)


=== Resultados Finais ===
Total de dias simulados: 45
Pico de infectados: 18078617
Total de recuperados: 4000091
Tempo total de execução: 282.44 segundos (4.71 minutos)

4 threads:

![image](https://github.com/user-attachments/assets/c8656c62-411c-4266-9ddb-8e3af2a46707)

![image](https://github.com/user-attachments/assets/23b179f5-b4b3-4014-ba8f-582089d57677)


=== Resultados Finais ===
Total de dias simulados: 45
Pico de infectados: 19023812
Total de recuperados: 4257662
Tempo total de execução: 179.41 segundos (2.99 minutos)


8 threads:

![image](https://github.com/user-attachments/assets/b7c457f8-9a83-4ee8-b868-332ec1ae0e43)

![image](https://github.com/user-attachments/assets/d2032567-fce7-48ae-89cf-871b95487ac3)


=== Resultados Finais ===
Total de dias simulados: 45
Pico de infectados: 18656057
Total de recuperados: 4134611
Tempo total de execução: 99.65 segundos (1.66 minutos)

16 threads:

![image](https://github.com/user-attachments/assets/0ec05086-c7f0-4885-9149-501e75b994aa)

![image](https://github.com/user-attachments/assets/c50dcaa6-80af-4455-abf3-1540a3012aa7)


=== Resultados Finais ===
Total de dias simulados: 45
Pico de infectados: 17171634
Total de recuperados: 3847913
Tempo total de execução: 64.44 segundos (1.07 minutos)



🧬 Simulação Paralela de Pandemia Baseada em Agentes
Um sistema de simulação epidemiológica que utiliza processamento paralelo para modelar a disseminação de uma pandemia em uma população massiva, com suporte a vacinação e análise temporal da infecção.

📋 Introdução
Este projeto implementa uma simulação baseada em agentes para modelar a propagação de uma doença infecciosa em larga escala. O objetivo principal é comparar a eficiência entre versões serial e paralela da simulação, demonstrando como técnicas de paralelismo podem melhorar significativamente o tempo de execução em cenários computacionalmente intensivos.

🎯 Descrição do Problema
Modelagens realistas de epidemias exigem a simulação de milhões de indivíduos, o que leva a tempos de execução elevados em abordagens sequenciais. Os principais desafios enfrentados foram:

🧠 Alta complexidade computacional: grande número de agentes interagindo diariamente.

🕒 Desempenho: necessidade de reduzir o tempo de simulação.

⚖️ Escalabilidade: capacidade de expandir para diferentes quantidades de núcleos de CPU.

💉 Eventos dinâmicos: como vacinação em massa em dias específicos.

🛠️ Descrição da Solução
🔄 Versão Serial
Simulação sequencial que processa interações entre agentes de forma linear, sendo usada como referência base para análise de performance.

🧵 Versão Paralela
Implementada com multiprocessing, a população é compartilhada via RawArray e os agentes infectados são divididos entre processos:

Distribuição balanceada das tarefas

Redução drástica no tempo de execução

Suporte para 2, 4, 8 e 16 processos simultâneos

⚙️ Configurações da Simulação
👥 População: 25.000.000

😷 Infectados Iniciais: 2.500.000

📆 Dias de Simulação: 45

💉 Vacinação em Massa: 500.000 pessoas no dia 1

📌 Taxa de Transmissão: 5%

📌 Taxa de Recuperação: 1%

🔁 Contatos por dia por infectado: 10

📊 Tabela de Performance
Versão	Tempo (s)	Processos	Speedup	Eficiência (%)
Serial	676.51	1	1.00	100.00
2 threads	282.44	2	2.40	119.76
4 threads	179.41	4	3.77	94.27
8 threads	99.65	8	6.79	84.86
16 threads	64.44	16	10.50	65.61

📈 Gráficos
📉 Speedup vs Número de Processos

📊 Eficiência vs Número de Processos

✅ Conclusão
A simulação paralela apresentou um desempenho significativamente superior à versão serial:

Principais Conquistas
🚀 Speedup de até 10.5x com 16 processos

⏱️ Tempo de execução reduzido de 676s para 64s

⚙️ Eficiência > 84% até 8 threads

🔄 Manutenção da dinâmica epidemiológica mesmo com paralelismo

Impacto
📉 Redução massiva no tempo de execução

🧪 Possibilidade de simular cenários mais complexos

🧩 Estrutura modular e escalável

Limitações Observadas
📉 Eficiência reduzida com mais de 8 processos devido ao overhead

🧠 Custo de sincronização e compartilhamento de memória entre processos

💻 Execução
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

# Paralelo (ex: com 8 processos)
python simulacao_paralela.py
👥 Autor
Welber Henrique
