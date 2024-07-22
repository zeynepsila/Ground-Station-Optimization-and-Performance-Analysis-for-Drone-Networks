import random
import math

class GreyWolfOptimizer:
    def __init__(self, num_wolves, max_iterations, a=1, A=2, C=1, b=1, l=1):
        self.num_wolves = num_wolves
        self.max_iterations = max_iterations
        self.a = a
        self.A = A
        self.C = C
        self.b = b
        self.l = l

    def optimize(self, stations, drones):
        best_global_position = None
        best_global_fitness = float('inf')

        wolves = []
        for _ in range(self.num_wolves):
            wolf = [(random.randint(0, len(stations) - 1), random.uniform(0, drone.max_battery_level)) for drone in drones]
            wolves.append(wolf)

        iteration = 0
        while iteration < self.max_iterations:
            for wolf in wolves:
                fitness = self.evaluate_fitness(wolf, drones, stations)
                if fitness < best_global_fitness:
                    best_global_fitness = fitness
                    best_global_position = wolf

                alpha, beta, delta = self.get_alpha_beta_delta(wolves, drones, stations)

                assigned_stations = set()
                assigned_drones = set()
                for i, (station_index, battery_level) in enumerate(wolf):
                    if station_index in assigned_stations or i in assigned_drones:
                        wolf[i] = (-1, battery_level)  # Atanmış istasyonu veya drone'u boşta olarak işaretle
                        continue

                    X1 = alpha[i][0]
                    X2 = beta[i][0]
                    X3 = delta[i][0]
                    D_alpha = abs(self.A * X1 - wolf[i][0])
                    D_beta = abs(self.A * X2 - wolf[i][0])
                    D_delta = abs(self.A * X3 - wolf[i][0])

                    X1_battery = alpha[i][1]
                    X2_battery = beta[i][1]
                    X3_battery = delta[i][1]
                    D_alpha_battery = abs(self.A * X1_battery - battery_level)
                    D_beta_battery = abs(self.A * X2_battery - battery_level)
                    D_delta_battery = abs(self.A * X3_battery - battery_level)

                    new_station_index = int(wolf[i][0] - self.a * (self.A * X1 - wolf[i][0]) - self.b * (self.A * X2 - wolf[i][0]) - self.l * (self.A * X3 - wolf[i][0]))
                    new_battery_level = battery_level - self.a * (self.A * X1_battery - battery_level) - self.b * (self.A * X2_battery - battery_level) - self.l * (self.A * X3_battery - battery_level)

                    new_station_index = max(0, min(new_station_index, len(stations) - 1))
                    new_battery_level = max(0, min(new_battery_level, drones[i].max_battery_level))

                    if new_station_index in assigned_stations or i in assigned_drones:
                        wolf[i] = (-1, new_battery_level)  # Atanmış istasyonu veya drone'u boşta olarak işaretle
                    else:
                        wolf[i] = (new_station_index, new_battery_level)
                        assigned_stations.add(new_station_index)
                        assigned_drones.add(i)

            iteration += 1

        return best_global_position, best_global_fitness

    def evaluate_fitness(self, wolf, drones, stations):
        total_fitness = 0
        assigned_stations = set()
        assigned_drones = set()

        for i, (station_index, battery_level) in enumerate(wolf):
            if station_index == -1:
                total_fitness += 1000  # Atanmamış drone için yüksek ceza ekle
                continue

            if station_index in assigned_stations or i in assigned_drones:
                total_fitness += 1000  # Birden fazla drone aynı istasyona veya aynı anda çalışıyorsa ceza ekle
                continue

            assigned_stations.add(station_index)
            assigned_drones.add(i)

            station_index = min(station_index, len(stations) - 1)
            if station_index < 0:
                station_index = 0
            if battery_level > drones[i].max_battery_level:
                battery_level = drones[i].max_battery_level
            elif battery_level < 0:
                battery_level = 0

            distance_to_station = math.sqrt((drones[i].x - stations[station_index].x) ** 2 + (drones[i].y - stations[station_index].y) ** 2)
            battery_fitness = 1 - (battery_level / drones[i].max_battery_level)
            fitness = (distance_to_station / drones[i].max_speed) + battery_fitness
            total_fitness += fitness

        return total_fitness

    def get_alpha_beta_delta(self, wolves, drones, stations):
        fitnesses = [self.evaluate_fitness(wolf, drones, stations) for wolf in wolves]
        sorted_fitnesses_indices = sorted(range(len(fitnesses)), key=lambda k: fitnesses[k])
        alpha_index = sorted_fitnesses_indices[0]
        beta_index = sorted_fitnesses_indices[1]
        delta_index = sorted_fitnesses_indices[2]

        return wolves[alpha_index], wolves[beta_index], wolves[delta_index]

    def iterate(self, stations, drones):
        current_solution = [(random.randint(0, len(stations) - 1), 0) for _ in range(len(drones))]
        current_fitness = self.evaluate_fitness(current_solution, drones, stations)
        return current_solution, current_fitness
