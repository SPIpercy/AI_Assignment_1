import random
import pandas as pd
import matplotlib.pyplot as plt

''' 
    generate_population function creates a array of dictionaries where all students are allocated randomly to each lecturer with respect to lecturer capacity
    
    POPULATION_SIZE = an integer that determines the number of dictionaries in the population array 
    supervisor_array = is the array that stores the student capacity of each lecturer
    student_array = is the array that stores an array with every student preference 
'''
def generate_population(POPULATION_SIZE, supervisor_array, student_array):
    population = []
    for i in range(POPULATION_SIZE):
        assign = {}
        supervisor_capacity = supervisor_array.copy()
        for student in range(len(student_array)):
            available_lecturers = [token for token, capacity in enumerate(supervisor_capacity) if capacity > 0]
            current_lecturer = random.choice(available_lecturers)
            assign[student] = current_lecturer + 1
            supervisor_capacity[current_lecturer] -= 1
        population.append(assign)
    return population
''' 
    the fitness_score function takes a dictionary out of the population array uses the student_dictionary, supervisor_dictionary to determine the preference position of the assigned
    lecturer for their assigned student and add their position in the preference to the fitness score 
   
   individual = one dictionary element from population
   student_dictionary = the dictionary that contains the preferences of each student  
   supervisor_dictionary = a dictionary that contains the capacity for each lecturer
'''
def fitness_score(individual, student_dictionary, supervisor_dictionary):
    fitness = 0
    lecturer_counts = [0]*len(supervisor_dictionary[1])
    for student, lecturer in individual.items():
        current_student = student_dictionary[student]
        for token, rank in enumerate(current_student.values()):
            current_lecturer = token + 1
            if current_lecturer == lecturer:
                fitness += rank - 1
                break
        lecturer_counts[lecturer-1] += 1
    for i, counter in enumerate(lecturer_counts):
        if counter > supervisor_dictionary[1][i]:
            fitness += 100
    return (fitness / len(individual))
''' 
    tournament_selection function takes 3 dictionaries from population and compares their fitness score against each other and returns the dictionary with the lowest score 
    
    population = collection of dictiories that contain the students and their allocated lecturer  
    fitness = the score produced from the fitness function and takes the position the lecturer is in the array of preference of each student and adding the position of the lecturer in the array
              and adds the position to the fitness score, the lower the better
'''
def tournament_selection(population, fitness):
    participants = random.sample(population, 3)
    tournament_fitness = [fitness[population.index(position)] for position in participants]
    return participants[tournament_fitness.index(min(tournament_fitness))]
''' 
   crossover function combines the two parents together at the crossover point to create two new individuals 

   parent_one = a individual that won the tournament selection (has the lowest fitness) 
   parent_two = another individual that won the tournament selection (has the lowest fitness) 
'''
def crossover(parent_one, parent_two):
    crossover_point = random.randint(1, len(parent_one) - 1)
    parent_one_keys= list(parent_one.keys())
    parent_two_keys = list(parent_two.keys())
    first_half_key_one = parent_one_keys[:crossover_point]
    second_half_key_one = parent_one_keys[crossover_point:]
    first_half_key_two = parent_two_keys[:crossover_point]
    second_half_key_two = parent_two_keys[crossover_point:]
    parent_one_dictionary_one = {key: parent_one[key] for key in first_half_key_one}
    parent_one_dictionary_two = {key: parent_one[key] for key in second_half_key_one}
    parent_two_dictionary_one = {key: parent_two[key] for key in first_half_key_two}
    parent_two_dictionary_two = {key: parent_two[key] for key in second_half_key_two}
    parent_one_dictionary_one.update(parent_two_dictionary_two)
    parent_two_dictionary_one.update(parent_one_dictionary_two)

    return parent_one_dictionary_one, parent_two_dictionary_one
'''
    the mutation function changes the assigned lecturer of two students and swaps them if the mutation rate is greater than a random number 
    
    individual = one dictionary element from population
    MUTATION_RATE = the value that determines how often mutation occurs
'''
def mutation(individual, MUTATION_RATE):
    if random.random() < MUTATION_RATE:
        position_one = random.randrange(len(individual))
        position_two = random.randrange(len(individual))
        if (position_one != position_two):
            position_one_value = individual[position_one]
           
            position_two_value = individual[position_two]
            individual[position_one] = position_two_value 
            individual[position_two] = position_one_value
    return individual
''' 
   The next_generation function creates a new population

   population = collection of dictiories that contain the students and their allocated lecturer
   fitness = the score produced from the fitness function and takes the position the lecturer is in the array of preference of each student and adding the position of the lecturer in the array
              and adds the position to the fitness score, the lower the better
   MUTATION_RATE = the value that determines how often mutation occurs
'''
def next_generation(population, fitness, MUTATION_RATE):
    new_population = []
    for _ in range(int(len(population) / 2)):
        parent_one = tournament_selection(population, fitness)
        parent_two = tournament_selection(population, fitness)
        child_one, child_two = crossover(parent_one, parent_two)
        child_one = mutation(child_one,MUTATION_RATE)
        child_two = mutation(child_two,MUTATION_RATE)
        new_population.append(child_one)
        new_population.append(child_two)

    return new_population
''' 
    genetic_algorithm is the main function that calculates the fitness for each generation and initialised the creation of the next generation and loops for the size of GENERATION

    GENERATION_SIZE = is the amount of times the genetic algorithm runs the other functions
    POPULATION_SIZE = an integer that determines the number of dictionaries in the population array 
    MUTATION_RATE = the value that determines how often mutation occurs
    student_dictionary = the dictionary that contains the preferences of each student  
    supervisor_dictionary = a dictionary that contains the capacity for each lecturer
    supervisor_array = is the array that stores the student capacity of each lecturer
    student_array = is the array that stores an array with every student preference
'''
def genetic_algorithm(GENERATION_SIZE, POPULATION_SIZE, MUTATION_RATE, student_dictionary, supervisor_dictionary, student_array, supervisor_array):
    population = generate_population(POPULATION_SIZE,supervisor_array,student_array)
    print(population)
    average_fitness = []
    best_score = 0
    worst_score = 0
    best_chromosone = {}
    average_fitness_per_generation = []
    for i in range(GENERATION_SIZE):
        population = sorted(population, key=lambda individual: fitness_score(individual, student_dictionary, supervisor_dictionary), reverse=False)

        total_score = 0
        for individual in population:
            fitness = fitness_score(individual, student_dictionary, supervisor_dictionary)
            average_fitness.append(fitness)

            if best_score > fitness:
                best_chromosone = individual

            best_score = min(best_score, fitness)
            worst_score = max(worst_score, fitness)
            total_score += fitness
        average_fitness_per_generation += [(total_score / len(population))]
        if fitness_score(population[0], student_dictionary, supervisor_dictionary) == 0.00:
            break
        population = next_generation(population, average_fitness, MUTATION_RATE)
    return best_chromosone, average_fitness_per_generation, best_score, worst_score
''' 
   main function extracts the informaton from the excel sheets and displays the information provided from the GA such as printing the best average fitness score for each generation,
   the worst average fitness score for each generation and the single best assignment of students and lecturers and out puts a graph that plots the average fitness over the generations
'''
def main():
    sc = pd.read_excel("Supervisors.xlsx", header=None)
    sp = pd.read_excel("Student-choices.xlsx", header=None)

    supervisors = sc.iloc[: , 1:]
    supervisor_dictionary = supervisors.to_dict()
    supervisor_array = supervisors.to_numpy().flatten()

    students = sp.iloc[: , 1:]
    student_dictionary = students.transpose().to_dict()
    student_array = students.to_numpy()
    student_array = [list(student_array[i]) for i in range(student_array.shape[0])]
    POPULATION_SIZE = 22
    GENERATION_SIZE = 46
    MUTATION_RATE = 0.01

    best_chromosone, avg_fitness_per_gen, best_score, worst_score = genetic_algorithm(GENERATION_SIZE, POPULATION_SIZE, MUTATION_RATE, student_dictionary, supervisor_dictionary, student_array, supervisor_array)
  
    print("\n The best fitness score: " + str(best_score))
    print("\n The worst fitness score: " + str(worst_score))
    print("\n Top 1 individual solution:\n\n " + str(best_chromosone))

    plt.plot(avg_fitness_per_gen)
    plt.xlabel("Generations")
    plt.ylabel("Average Fitness")

main()