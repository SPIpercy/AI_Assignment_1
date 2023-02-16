import random
import matplotlib.pyplot as plt

def create_population(size, chromosome_size):
    """Create a population of `size` chromosomes"""
    return [''.join(random.choices(['0', '1'], k=chromosome_size)) for _ in range(size)]

def fitness(chromosome, chromosome_size):
    """Evaluate the fitness of a chromosome"""
    if chromosome == "0" * chromosome_size:
        return 2*chromosome_size
    else:
        return sum(int(gene) for gene in chromosome)

def tournament_selection(population, fitness, tournament_size):
    competitors = random.sample(population, tournament_size)

    competitors_fitness = [fitness[population.index(i)] for i in competitors]
    return population[population.index(competitors[competitors_fitness.index(max(competitors_fitness))])]

def crossover(parent1, parent2, crossover_point):
    offspring1 = parent1[:crossover_point] + parent2[crossover_point:]
    offspring2 = parent2[:crossover_point] + parent1[crossover_point:]
    return offspring1, offspring2


def mutate(chromosome, mutation_prob):
    """Mutate the chromosome with a probability of `mutation_prob`"""
    chromosome = list(chromosome)
    for i in range(len(chromosome)):
        if random.uniform(0, 1) < mutation_prob:
            chromosome[i] = '1' if chromosome[i] == '0' else '0'
    return ''.join(chromosome)

def generate_offspring(avg_fitness, population, population_size, chromosome_length, tournament_size, mutation_prob):
    fitness = avg_fitness

    offspring = []
    while len(offspring) < population_size:
        parent1 = tournament_selection(population, fitness, tournament_size)
        parent2 = tournament_selection(population, fitness, tournament_size)
        
        crossover_point = random.randint(1, chromosome_length - 1)
        offspring1, offspring2 = crossover(parent1, parent2, crossover_point)
        offspring.append(mutate(offspring1, mutation_prob))
        offspring.append(mutate(offspring2, mutation_prob))
    return offspring[:population_size]

def genetic_algorithm(population_size, num_generations, chromosome_size, mutation_prob,tournament_size):
    """Perform the genetic algorithm"""
    population = create_population(population_size, chromosome_size)

    avg_fitness_per_gen = []

    for generation in range(num_generations):
        avg_fitness = [(fitness(individual, chromosome_size)) for individual in population]
        avg_fitness_per_gen.append(sum(avg_fitness)/population_size)
        population = generate_offspring(avg_fitness,population, population_size, chromosome_size, tournament_size, mutation_prob)
        population[5] = ("0"*chromosome_size)
    return avg_fitness_per_gen

def main():
    population_size = 15
    num_generations = 100
    chromosome_size = 30
    mutation_prob = 0.01
    tournament_size = 5
    avg_fitness = genetic_algorithm(population_size, num_generations, chromosome_size, mutation_prob,tournament_size)

    plt.plot(avg_fitness)
    plt.xlabel('Generation')
    plt.ylabel('Average Fitness')
    plt.show()

main()
