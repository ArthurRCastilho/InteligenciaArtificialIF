import numpy as np
import matplotlib.pyplot as plt
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import random

# Entradas
peso = ctrl.Antecedent(np.arange(0, 21, 1), 'peso')
sujeira = ctrl.Antecedent(np.arange(0, 11, 1), 'sujeira')
tecido = ctrl.Antecedent(np.arange(0, 11, 1), 'tecido')

# Saída
tempo = ctrl.Consequent(np.arange(0, 121, 1), 'tempo')

# Funções de pertinência para peso
peso['leve'] = fuzz.trimf(peso.universe, [0, 0, 8])
peso['medio'] = fuzz.trimf(peso.universe, [4, 10, 16])
peso['pesado'] = fuzz.trimf(peso.universe, [12, 20, 20])

# Funções de pertinência para sujeira
sujeira['baixa'] = fuzz.trimf(sujeira.universe, [0, 0, 4])
sujeira['media'] = fuzz.trimf(sujeira.universe, [2, 5, 8])
sujeira['alta'] = fuzz.trimf(sujeira.universe, [6, 10, 10])

# Funções de pertinência para tecido
tecido['delicado'] = fuzz.trimf(tecido.universe, [0, 0, 4])
tecido['normal'] = fuzz.trimf(tecido.universe, [2, 5, 8])
tecido['pesado'] = fuzz.trimf(tecido.universe, [6, 10, 10])

# Funções de pertinência para tempo
tempo['curto'] = fuzz.trimf(tempo.universe, [0, 0, 40])
tempo['medio'] = fuzz.trimf(tempo.universe, [30, 60, 90])
tempo['longo'] = fuzz.trimf(tempo.universe, [80, 120, 120])

# Regras
regra1 = ctrl.Rule(peso['leve'] & sujeira['baixa'] & tecido['delicado'], tempo['curto'])
regra2 = ctrl.Rule(peso['medio'] & sujeira['media'] & tecido['normal'], tempo['medio'])
regra3 = ctrl.Rule(peso['pesado'] & sujeira['alta'] & tecido['pesado'], tempo['longo'])
regra4 = ctrl.Rule(sujeira['alta'] & tecido['delicado'], tempo['medio'])
regra5 = ctrl.Rule(peso['pesado'] | sujeira['alta'], tempo['longo'])
regra6 = ctrl.Rule(tecido['delicado'] & sujeira['baixa'], tempo['curto'])

# Novas regras para melhor cobertura
regra7 = ctrl.Rule(peso['leve'] & sujeira['media'], tempo['medio'])
regra8 = ctrl.Rule(peso['medio'] & sujeira['baixa'], tempo['curto'])
regra9 = ctrl.Rule(peso['pesado'] & sujeira['baixa'], tempo['medio'])
regra10 = ctrl.Rule(peso['leve'] & sujeira['alta'], tempo['medio'])
regra11 = ctrl.Rule(tecido['pesado'] & peso['pesado'], tempo['longo'])
regra12 = ctrl.Rule(tecido['delicado'] & peso['leve'], tempo['curto'])

# Sistema de controle
sistema_lavagem_ctrl = ctrl.ControlSystem([regra1, regra2, regra3, regra4, regra5, regra6, 
                                         regra7, regra8, regra9, regra10, regra11, regra12])
sistema_lavagem = ctrl.ControlSystemSimulation(sistema_lavagem_ctrl)

# Mapa de entradas original com comentários
entradas = [
    {'peso': 2, 'sujeira': 2, 'tecido': 2},  # Leve, pouco sujo, delicado
    {'peso': 5, 'sujeira': 5, 'tecido': 5},  # Médio, média sujeira, normal
    {'peso': 9, 'sujeira': 9, 'tecido': 9},  # Pesado, muito sujo, tecido pesado
    {'peso': 6, 'sujeira': 8, 'tecido': 3},  # Pesado, muito sujo, delicado
    {'peso': 1, 'sujeira': 9, 'tecido': 1},  # Leve, muito sujo, delicado
]

# Criando um novo mapa com entradas aleatórias
entradas_aleatorias = []
for _ in range(5):
    entrada = {
        'peso': random.uniform(0, 20),
        'sujeira': random.uniform(0, 10),
        'tecido': random.uniform(0, 10)
    }
    entradas_aleatorias.append(entrada)

# Usando as entradas aleatórias para o sistema
tempos = []
labels = []

# Processando as entradas aleatórias
for i, entrada in enumerate(entradas):
    try:
        sistema_lavagem.input['peso'] = entrada['peso']
        sistema_lavagem.input['sujeira'] = entrada['sujeira']
        sistema_lavagem.input['tecido'] = entrada['tecido']
        sistema_lavagem.compute()
        
        # Verificando se o tempo foi calculado
        if 'tempo' in sistema_lavagem.output:
            tempos.append(sistema_lavagem.output['tempo'])
            labels.append(f"P:{entrada['peso']:.1f} S:{entrada['sujeira']:.1f} T:{entrada['tecido']:.1f}")
        else:
            # Se não conseguir calcular, usa um valor padrão
            tempos.append(60)  # Tempo médio como fallback
            labels.append(f"P:{entrada['peso']:.1f} S:{entrada['sujeira']:.1f} T:{entrada['tecido']:.1f} (fallback)")
    except Exception as e:
        print(f"Erro ao processar entrada {i+1}: {str(e)}")
        tempos.append(60)  # Tempo médio como fallback
        labels.append(f"P:{entrada['peso']:.1f} S:{entrada['sujeira']:.1f} T:{entrada['tecido']:.1f} (erro)")

# Gráfico comparativo
plt.figure(figsize=(10, 6))
plt.bar(labels, tempos, color='skyblue')
plt.title("Comparação do Tempo de Lavagem para Diferentes Entradas Fuzzy")
plt.xlabel("Entradas (Peso, Sujeira, Tecido)")
plt.ylabel("Tempo de Lavagem (minutos)")
plt.ylim(0, 125)
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.show()

