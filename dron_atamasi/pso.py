import random
import time
import math
import matplotlib.pyplot as plt

class PSO:
    def __init__(self, num_particles, max_iterations, inertia_weight, cognitive_weight, social_weight):
        self.num_particles = num_particles
        self.max_iterations = max_iterations
        self.inertia_weight = inertia_weight
        self.cognitive_weight = cognitive_weight
        self.social_weight = social_weight

    def optimize(self, stations, drones):
        global start_time
        start_time = time.time()  # start_time burada tanımlandı

        best_global_position = [(0, 0) for _ in drones]
        best_global_fitness = float('inf')

        particles = []
        for _ in range(self.num_particles):
            particle = [(random.uniform(0, len(stations)), random.uniform(0, drone.max_battery_level)) for drone in drones]
            particles.append(particle)

        fitness_values = []  # Her iterasyondaki ortalama fitness değerlerini saklamak için liste

        iteration = 0
        while iteration < self.max_iterations:
            iteration_fitness_values = []  # Bu iterasyondaki fitness değerleri
            for i, particle in enumerate(particles):
                fitness = self.evaluate_fitness(particle, drones, stations)
                iteration_fitness_values.append(fitness)
                if fitness < best_global_fitness:
                    best_global_fitness = fitness
                    best_global_position = particle

                assigned_stations = set()
                assigned_drones = set()

                for j, (station_index, battery_level) in enumerate(particle):
                    station_index = int(station_index)

                    if station_index < len(stations) and station_index not in assigned_stations:
                        inertia_term = self.inertia_weight * station_index
                        cognitive_term = self.cognitive_weight * random.random() * (station_index - best_global_position[j][0])
                        social_term = self.social_weight * random.random() * (station_index - best_global_position[j][0])
                        new_station_index = inertia_term + cognitive_term + social_term
                        new_station_index = int(min(max(new_station_index, 0), len(stations) - 1))

                        if new_station_index not in assigned_stations:
                            particle[j] = (new_station_index, battery_level)
                            assigned_stations.add(new_station_index)
                            assigned_drones.add(j)
                        else:
                            available_stations = [idx for idx in range(len(stations)) if idx not in assigned_stations]
                            if available_stations:
                                new_station_index = random.choice(available_stations)
                                particle[j] = (new_station_index, battery_level)
                                assigned_stations.add(new_station_index)
                    else:
                        particle[j] = (-1, battery_level)

                for idx in range(len(drones)):
                    if idx not in assigned_drones:
                        pass  # Cezai işlem eklenebilir

            # Her iterasyondaki ortalama fitness değerini sakla
            average_fitness = sum(iteration_fitness_values) / len(iteration_fitness_values)
            fitness_values.append(average_fitness)

            iteration += 1

        end_time = time.time()  # end_time burada tanımlandı
        elapsed_time = end_time - start_time  # elapsed_time hesaplandı

        # En iyi pozisyonu ve uygunluğu döndür
        unassigned_drones = [i for i, (station_index, _) in enumerate(best_global_position) if station_index == -1]
        return best_global_position, best_global_fitness, fitness_values, elapsed_time

    def evaluate_fitness(self, particle, drones, stations):
        total_fitness = 0
        for i, drone in enumerate(drones):
            station_index, battery_level = particle[i]
            station_index = int(station_index)

            if station_index >= 0 and station_index < len(stations):
                distance_to_station = math.sqrt((drone.x - stations[station_index].x) ** 2 + (drone.y - stations[station_index].y) ** 2)
                battery_fitness = 1 - (battery_level / drone.max_battery_level)
                fitness = (distance_to_station / drone.max_speed) + battery_fitness
            else:
                fitness = 100  # Eğer dron hiçbir istasyona atanmazsa ceza uygulanabilir

            total_fitness += fitness

        return total_fitness
    