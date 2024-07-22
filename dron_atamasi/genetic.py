import random
import math
import matplotlib.pyplot as plt

class GeneticAlgorithm:
    def __init__(self, population_size, mutation_rate, crossover_rate, max_generations):
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.max_generations = max_generations

    def initialize_population(self, drones, stations):
        population = []
        for _ in range(self.population_size):
            individual = []
            for drone in drones:
                station_index = random.randint(-1, len(stations) - 1)  # Allow -1 for unassigned
                battery_level = random.uniform(0, drone.max_battery_level)
                individual.append((station_index, battery_level))
            population.append(individual)
        return population

    def evaluate_fitness(self, individual, drones, stations):
        total_fitness = 0
        for i, drone in enumerate(drones):
            station_index, battery_level = individual[i]
            station_index = int(station_index)
            
            if station_index == -1:
                fitness = 10  # Penalty value for unassigned drones
            else:
                distance_to_station = math.sqrt((drone.x - stations[station_index].x) ** 2 + (drone.y - stations[station_index].y) ** 2)
                battery_fitness = 1 - (battery_level / drone.max_battery_level)
                fitness = (distance_to_station / drone.max_speed) + battery_fitness
                
            total_fitness += fitness
        return total_fitness

    def select_parents(self, population, fitnesses):
        total_fitness = sum(fitnesses)
        selection_probs = [f / total_fitness for f in fitnesses]
        parents = random.choices(population, weights=selection_probs, k=2)
        return parents

    def crossover(self, parent1, parent2):
        if random.random() < self.crossover_rate:
            crossover_point = random.randint(1, len(parent1) - 1)
            child1 = parent1[:crossover_point] + parent2[crossover_point:]
            child2 = parent2[:crossover_point] + parent1[crossover_point:]
            return child1, child2
        else:
            return parent1, parent2

    def mutate(self, individual, drones, stations):
        for i in range(len(individual)):
            if random.random() < self.mutation_rate:
                station_index = random.randint(-1, len(stations) - 1)  # Allow -1 for unassigned
                battery_level = random.uniform(0, drones[i].max_battery_level)
                individual[i] = (station_index, battery_level)
        return individual



    def optimize(self, drones, stations):
        population = self.initialize_population(drones, stations)
        fitness_history = []

        for generation in range(self.max_generations):
            fitnesses = [self.evaluate_fitness(individual, drones, stations) for individual in population]
            new_population = []

            while len(new_population) < self.population_size:
                parent1, parent2 = self.select_parents(population, fitnesses)
                child1, child2 = self.crossover(parent1, parent2)
                child1 = self.mutate(child1, drones, stations)
                child2 = self.mutate(child2, drones, stations)
                new_population.extend([child1, child2])

            population = new_population[:self.population_size]
            best_solution = min(population, key=lambda ind: self.evaluate_fitness(ind, drones, stations))
            best_fitness = self.evaluate_fitness(best_solution, drones, stations)

            fitness_history.append(best_fitness)

        return best_solution, best_fitness, fitness_history