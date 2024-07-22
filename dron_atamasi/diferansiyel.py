import tkinter as tk
import random
import time
import math
import matplotlib.pyplot as plt

class DEA:
    def __init__(self, num_particles, max_iterations, scaling_factor, crossover_rate):
        self.num_particles = num_particles
        self.max_iterations = max_iterations
        self.scaling_factor = scaling_factor
        self.crossover_rate = crossover_rate

    def optimize(self, stations, drones):
        global start_time
        start_time = time.time()

        best_global_position = [(0, 0) for _ in drones]
        best_global_fitness = float('inf')

        particles = []
        for _ in range(self.num_particles):
            particle = [(random.uniform(0, len(stations)), random.uniform(0, drone.max_battery_level)) for drone in drones]
            particles.append(particle)

        fitness_values = []

        iteration = 0
        while iteration < self.max_iterations:
            for i in range(len(particles)):
                trial_vector = self.generate_trial_vector(particles, i, self.scaling_factor, stations, drones)

                # Ensure one-to-one assignment or unassigned
                assigned_stations = set()
                for j, (station_index, battery_level) in enumerate(trial_vector):
                    if station_index != -1 and int(station_index) in assigned_stations:
                        available_stations = [idx for idx in range(len(stations)) if idx not in assigned_stations]
                        if available_stations:
                            trial_vector[j] = (random.choice(available_stations), battery_level)
                        else:
                            trial_vector[j] = (-1, battery_level)  # Unassign if no stations available
                    assigned_stations.add(int(station_index))

                # Crossover
                crossover_point = random.randint(0, len(particles[i]) - 1)
                new_particle = []
                for j in range(len(particles[i])):
                    if random.random() < self.crossover_rate or j == crossover_point:
                        new_particle.append(trial_vector[j])
                    else:
                        new_particle.append(particles[i][j])

                fitness = self.evaluate_fitness(new_particle, drones, stations)
                if fitness < self.evaluate_fitness(particles[i], drones, stations):
                    particles[i] = new_particle

                if fitness < best_global_fitness:
                    best_global_fitness = fitness
                    best_global_position = new_particle

            average_fitness = sum([self.evaluate_fitness(p, drones, stations) for p in particles]) / len(particles)
            fitness_values.append(average_fitness)

            iteration += 1

        end_time = time.time()
        elapsed_time = end_time - start_time

        unassigned_drones = [i for i, (station_index, _) in enumerate(best_global_position) if station_index == -1]
        return best_global_position, best_global_fitness, fitness_values, elapsed_time

    def generate_trial_vector(self, particles, current_index, scaling_factor, stations, drones):
        indexes = list(range(len(particles)))
        indexes.remove(current_index)
        random.shuffle(indexes)

        a, b, c = indexes[0], indexes[1], indexes[2]

        trial_vector = []
        for j in range(len(particles[current_index])):
            x_a, x_b, x_c = particles[a][j], particles[b][j], particles[c][j]

            new_station_index = x_a[0] + scaling_factor * (x_b[0] - x_c[0])
            new_battery_level = x_a[1] + scaling_factor * (x_b[1] - x_c[1])

            # Ensure valid station index or unassigned
            if random.random() < 0.1:  # Small probability of being unassigned
                new_station_index = -1
            else:
                new_station_index = min(max(new_station_index, 0), len(stations) - 1)

            new_battery_level = min(max(new_battery_level, 0), drones[j].max_battery_level)

            trial_vector.append((new_station_index, new_battery_level))

        return trial_vector

    def evaluate_fitness(self, particle, drones, stations):
        total_fitness = 0
        assigned_stations = set()
        for i, drone in enumerate(drones):
            station_index, battery_level = particle[i]
            station_index = int(station_index)

            if station_index >= 0 and station_index < len(stations) and station_index not in assigned_stations:
                distance_to_station = math.sqrt((drone.x - stations[station_index].x) ** 2 + (drone.y - stations[station_index].y) ** 2)
                battery_fitness = 1 - (battery_level / drone.max_battery_level)
                fitness = (distance_to_station / drone.max_speed) + battery_fitness
                assigned_stations.add(station_index)
            else:
                fitness = 100

            total_fitness += fitness

        return total_fitness
