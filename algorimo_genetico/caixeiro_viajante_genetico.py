import random
import numpy as np
import matplotlib.pyplot as plt

# Criação da Matriz quadrada de Distancia entre as cidades
def create_distance_matrix(num_cities):
    return np.random.randint(10, 100, size=(num_cities, num_cities))

# Número de soluções de rotas
def create_initial_population(pop_size, num_cities):
    return [random.sample(range(num_cities), num_cities) for _ in range(pop_size)]

# Cálculo de custo de uma rota
def fitness(route, distance_matrix):
    return sum(distance_matrix[route[i], route[i+1]] for i in range(len(route)-1)) + distance_matrix[route[-1], route[0]]
# Soma as distâncias entre cidades consecutivas e incluindo o retorno à cidade inicial.

# Seleção dos Pais
def select_parents(population, distance_matrix, best_parents_rate=0.6):
    pais_aleatorios = random.sample(population, 2)

    if random.random() < best_parents_rate:
        pais_ordenados = sorted(population, key=lambda x: fitness(x, distance_matrix))[:2]
        return pais_ordenados
    
    return pais_aleatorios

# Recombinação Genética (Crossover)
def crossover(parent1, parent2):
    cut = len(parent1) // 2
    return parent1[:cut] + [city for city in parent2 if city not in parent1[:cut]]

# Mutação
# def mutate(route):
#     i, j = random.sample(range(len(route)), 2)  # Troca aleatória de duas cidades
#     route[i], route[j] = route[j], route[i]
#     return route

# Mutação com probabilidade
def mutate(route, mutation_rate=0.1):
    if random.random() < mutation_rate:
        i, j = random.sample(range(len(route)), 2) # Troca aleatória de duas cidades
        route[i], route[j] = route[j], route[i]
    return route


# Algoritmo Genético
def genetic_algorithm(num_cities=20, pop_size=100, generations=100):
    distance_matrix = create_distance_matrix(num_cities)  # Inicializa a matriz de distância
    population = create_initial_population(pop_size, num_cities)  # Inicializa a população
    
    best_distances = []  # Lista para armazenar a melhor distância por geração

    for gen in range(generations):  # Para cada geração
        parents = select_parents(population, distance_matrix)  # Seleciona os pais
        offspring = [mutate(crossover(parents[0], parents[1])) for _ in range(pop_size - len(parents))]  # Gera filhos
        population = parents + offspring  # Atualiza a população

        # Melhor solução da geração atual
        best_route = min(population, key=lambda x: fitness(x, distance_matrix))
        best_distance = fitness(best_route, distance_matrix)
        best_distances.append(best_distance)  # Salva a melhor distância da geração

        # Printando a melhor solução da geração
        print(f'Geração {gen + 1}: Melhor rota: {best_route}, Distância: {best_distance}')

    # Melhor solução final
    return best_route, best_distance, best_distances

# Executa o algoritmo
best_route, best_distance, best_distances = genetic_algorithm()

print("-----------------------")
print(f'Melhor rota: {best_route}\nDistância: {best_distance}')

# Gráfico da evolução da melhor distância
plt.plot(range(1, len(best_distances) + 1), best_distances, marker='o', linestyle='-', color='b', label='Melhor Distância')
plt.xlabel('Geração')
plt.ylabel('Melhor Distância')
plt.title('Evolução da Melhor Distância ao Longo das Gerações')
plt.legend()
plt.grid()
plt.show()
