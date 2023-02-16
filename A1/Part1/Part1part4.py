import random
import matplotlib.pyplot as plt

def create_target(chromosome_size):
    """Create a population of `size` chromosomes"""
    return ''.join(random.choices(['0', '1','2', '3','4', '5','6', '7','8', '9'], k=chromosome_size))

def create_population(size, chromosome_size):
    """Create a population of `size` chromosomes"""
    return [''.join(random.choices(['0', '1','2', '3','4', '5','6', '7','8', '9'], k=chromosome_size)) for _ in range(size)]

def fitness(chromosome,target):
    count = 0
    
    for i in range(len(target)):
        if chromosome[i] == target[i]:
            count += 1
    return count

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
            if chromosome[i] == '0':
               chromosome[i] = ''.join(random.choices(['1','2','3','4','5','6','7','8','9']))
            elif chromosome[i] == '1':
                chromosome[i] = ''.join(random.choices(['0','2','3','4','5','6','7','8','9']))
            elif chromosome[i] == '2':
               chromosome[i] = ''.join(random.choices(['0','1','3','4','5','6','7','8','9']))
            elif chromosome[i] == '3':
                chromosome[i] = ''.join(random.choices(['0','1','2','4','5','6','7','8','9']))
            elif chromosome[i] == '4':
                chromosome[i] = ''.join(random.choices(['0','1','2','3','5','6','7','8','9']))
            elif chromosome[i] == '5':
               chromosome[i] = ''.join(random.choices(['0','1','2','3','4','6','7','8','9']))
            elif chromosome[i] == '6':
                chromosome[i] = ''.join(random.choices(['0','1','2','3','4','5','7','8','9']))
            elif chromosome[i] == '7':
                chromosome[i] = ''.join(random.choices(['0','1','2','3','4','5','6','8','9']))
            elif chromosome[i] == '8':
               chromosome[i] = ''.join(random.choices(['0','1','2','3','4','5','6','7','9']))
            elif chromosome[i] == '9':
               chromosome[i] = ''.join(random.choices(['0','1','2','3','4','5','6','7','8',]))
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

def genetic_algorithm(population_size, num_generations, chromosome_size, mutation_prob,tournament_size, target):
    """Perform the genetic algorithm"""
    population = create_population(population_size, chromosome_size)

    avg_fitness_per_gen = []

    for generation in range(num_generations):
        avg_fitness = [(fitness(individual, target)) for individual in population]
        avg_fitness_per_gen.append(sum(avg_fitness)/population_size)
        population = generate_offspring(avg_fitness,population, population_size, chromosome_size, tournament_size, mutation_prob)
    return avg_fitness_per_gen

def main():

    population_size = 15
    num_generations = 100
    chromosome_size = 30
    mutation_prob = 0.01
    tournament_size = 5
    target = create_target(chromosome_size)

    avg_fitness = genetic_algorithm(population_size, num_generations, chromosome_size, mutation_prob,tournament_size, target)

    plt.plot(avg_fitness)
    plt.xlabel('Generation')
    plt.ylabel('Average Fitness')
    plt.show()

main()