import random
import math
import matplotlib.pyplot as plt

class ABC:
    def __init__(self, num_employed_bees, num_onlooker_bees, max_iterations, limit, stations, drones):
        self.num_employed_bees = num_employed_bees
        self.num_onlooker_bees = num_onlooker_bees
        self.max_iterations = max_iterations
        self.limit = limit
        self.stations = stations
        self.drones = drones
        self.best_solution = None
        self.best_fitness = float('inf')
        self.trial_counters = [0] * self.num_employed_bees
        self.best_fitness_per_iteration = []

    def optimize(self):
        employed_bees = []
        for _ in range(self.num_employed_bees):
            solution = self.generate_random_solution()
            fitness = self.evaluate_fitness(solution)
            employed_bees.append((solution, fitness))

        iteration = 0
        while iteration < self.max_iterations:
            # Employed Bee Phase
            for i, (solution, _) in enumerate(employed_bees):
                new_solution = self.explore_neighbor(solution)
                new_fitness = self.evaluate_fitness(new_solution)
                if new_fitness < employed_bees[i][1]:
                    employed_bees[i] = (new_solution, new_fitness)
                    self.trial_counters[i] = 0
                else:
                    self.trial_counters[i] += 1

            # Onlooker Bee Phase
            for _ in range(self.num_onlooker_bees):
                bee_index = self.select_bee(employed_bees)
                solution, _ = employed_bees[bee_index]
                new_solution = self.explore_neighbor(solution)
                new_fitness = self.evaluate_fitness(new_solution)
                if new_fitness < employed_bees[bee_index][1]:
                    employed_bees[bee_index] = (new_solution, new_fitness)
                    self.trial_counters[bee_index] = 0
                else:
                    self.trial_counters[bee_index] += 1

            # Scout Bee Phase
            for i in range(self.num_employed_bees):
                if self.trial_counters[i] > self.limit:
                    new_solution = self.generate_random_solution()
                    employed_bees[i] = (new_solution, self.evaluate_fitness(new_solution))
                    self.trial_counters[i] = 0

            # Best solution update
            for solution, fitness in employed_bees:
                if fitness < self.best_fitness:
                    self.best_solution = solution
                    self.best_fitness = fitness

            # Record the best fitness of this iteration
            self.best_fitness_per_iteration.append(self.best_fitness)
            iteration += 1

        return self.best_solution, self.best_fitness, self.best_fitness_per_iteration

    def generate_random_solution(self):
        available_stations = list(range(len(self.stations)))
        solution = []
        for drone in self.drones:
            if available_stations:
                station_index = random.choice(available_stations)
                available_stations.remove(station_index)
                battery_level = random.uniform(0, drone.max_battery_level)
            else:
                station_index = -1
                battery_level = 0
            solution.append((station_index, battery_level))
        return solution

    def explore_neighbor(self, solution):
        new_solution = []
        available_stations = list(range(len(self.stations)))
        random.shuffle(available_stations)
        for station_index, battery_level in solution:
            if station_index == -1 or len(available_stations) == 0:
                new_station_index = -1
            else:
                if station_index in available_stations:
                    available_stations.remove(station_index)
                if available_stations:
                    new_station_index = random.choice(available_stations)
                    available_stations.remove(new_station_index)
                else:
                    new_station_index = -1
            new_battery_level = random.uniform(0, self.drones[0].max_battery_level)
            new_solution.append((new_station_index, new_battery_level))
        return new_solution

    def evaluate_fitness(self, solution):
        if solution is None:
            return float('inf')
        total_fitness = 0
        for i, drone in enumerate(self.drones):
            if solution[i] is None:
                continue
            station_index, battery_level = solution[i]
            station_index = int(station_index)

            if station_index >= 0 and station_index < len(self.stations):
                distance_to_station = math.sqrt((drone.x - self.stations[station_index].x) ** 2 + (drone.y - self.stations[station_index].y) ** 2)
                battery_fitness = 1 - (battery_level / drone.max_battery_level)
                fitness = (distance_to_station / drone.max_speed) + battery_fitness
            else:
                fitness = 100

            total_fitness += fitness

        return total_fitness

    def select_bee(self, bees):
        total_fitness = sum(1 / fitness for _, fitness in bees if fitness > 0)
        rand_val = random.uniform(0, total_fitness)
        temp_sum = 0
        for i, (_, fitness) in enumerate(bees):
            if fitness > 0:
                temp_sum += 1 / fitness
            if temp_sum >= rand_val:
                return i

