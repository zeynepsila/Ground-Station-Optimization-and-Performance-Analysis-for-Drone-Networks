import random
import math
import matplotlib.pyplot as plt
import time
import tkinter as tk
from tkinter import ttk

class Drone:
    def __init__(self, x, y, max_battery_level, max_speed):
        self.x = x
        self.y = y
        self.max_battery_level = max_battery_level
        self.max_speed = max_speed

class Station:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class GOA:
    def __init__(self, population_size, max_iterations):
        self.population_size = population_size
        self.max_iterations = max_iterations

    def optimize(self, drones, stations):
        best_global_position = [(0, 0) for _ in drones]
        best_global_fitness = float('inf')

        grasshoppers = []
        for _ in range(self.population_size):
            grasshopper = [(random.uniform(0, len(stations) - 1), random.uniform(0, drone.max_battery_level)) for drone in drones]
            grasshoppers.append(grasshopper)

        iteration = 0
        fitness_history = []
        all_fitness_values = []
        avg_fitness_history = []

        while iteration < self.max_iterations:
            iteration_fitness_values = []
            for i, grasshopper in enumerate(grasshoppers):
                fitness = self.evaluate_fitness(grasshopper, drones, stations)
                iteration_fitness_values.append(fitness)
                if fitness < best_global_fitness:
                    best_global_fitness = fitness
                    best_global_position = grasshopper

                assigned_stations = set()
                assigned_drones = set()

                for j, (station_index, battery_level) in enumerate(grasshopper):
                    station_index = int(station_index)

                    if station_index < len(stations) and station_index not in assigned_stations:
                        inertia_term = random.uniform(0, 1) * station_index
                        cognitive_term = random.uniform(0, 1) * (station_index - best_global_position[j][0])
                        social_term = random.uniform(0, 1) * (station_index - best_global_position[j][0])
                        new_station_index = inertia_term + cognitive_term + social_term
                        new_station_index = int(min(max(new_station_index, 0), len(stations) - 1))

                        if new_station_index not in assigned_stations:
                            grasshopper[j] = (new_station_index, battery_level)
                            assigned_stations.add(new_station_index)
                            assigned_drones.add(j)
                        else:
                            available_stations = [idx for idx in range(len(stations)) if idx not in assigned_stations]
                            if available_stations:
                                new_station_index = random.choice(available_stations)
                                grasshopper[j] = (new_station_index, battery_level)
                                assigned_stations.add(new_station_index)
                    else:
                        grasshopper[j] = (-1, battery_level)

            iteration += 1
            fitness_history.append(best_global_fitness)
            all_fitness_values.append(iteration_fitness_values)
            avg_fitness_history.append(sum(iteration_fitness_values) / len(iteration_fitness_values))

        unassigned_drones = [i for i, (station_index, _) in enumerate(best_global_position) if station_index == -1]
        return best_global_position, best_global_fitness, fitness_history, all_fitness_values, avg_fitness_history, unassigned_drones

    def evaluate_fitness(self, grasshopper, drones, stations):
        total_fitness = 0
        for i, drone in enumerate(drones):
            station_index, battery_level = grasshopper[i]
            station_index = int(station_index)

            if station_index >= 0 and station_index < len(stations):
                distance_to_station = math.sqrt((drone.x - stations[station_index].x) ** 2 + (drone.y - stations[station_index].y) ** 2)
                battery_fitness = 1 - (battery_level / drone.max_battery_level)
                fitness = (distance_to_station / drone.max_speed) + battery_fitness
            else:
                fitness = 100

            total_fitness += fitness

        return total_fitness


