import random
import math
import matplotlib.pyplot as plt

class AntColonyOptimization:
    def __init__(self, num_ants, num_iterations, evaporation_rate, alpha, beta, pheromone_deposit, initial_pheromone):
        self.num_ants = num_ants
        self.num_iterations = num_iterations
        self.evaporation_rate = evaporation_rate
        self.alpha = alpha
        self.beta = beta
        self.pheromone_deposit = pheromone_deposit
        self.initial_pheromone = initial_pheromone
        self.best_fitness = float('inf')  # En iyi uygunluk değeri, ilk çözümle başlayacak
        self.pheromones = None
    
    def optimize(self, stations, drones):
        num_stations = len(stations)
        self.pheromones = [[self.initial_pheromone] * num_stations for _ in range(num_stations)]
        
        # İlk çözüm ve uygunluk değerini başlangıç olarak ayarla
        initial_solution = self.construct_solutions(stations, drones)[0]
        self.best_solution = initial_solution
        self.best_fitness = self.calculate_fitness(initial_solution, stations)
        
        fitness_history = [self.best_fitness]  # Her iterasyonun en iyi uygunluk değerlerini saklamak için
        average_fitness_history = [self.best_fitness]  # Her iterasyonun ortalama uygunluk değerlerini saklamak için

        for iteration in range(self.num_iterations):
            solutions = self.construct_solutions(stations, drones)
            self.update_pheromones(solutions)
            iteration_best_solution, iteration_best_fitness = self.get_best_solution(solutions, stations)
            
            # Her iterasyonun en iyi uygunluk değerini sakla
            fitness_history.append(iteration_best_fitness)
            
            # Her iterasyondaki ortalama fitness değerini hesapla
            average_fitness = sum(fitness_history) / len(fitness_history)
            average_fitness_history.append(average_fitness)
            
            if iteration_best_fitness < self.best_fitness:
                self.best_fitness = iteration_best_fitness
                self.best_solution = iteration_best_solution
            
        return self.best_solution, self.best_fitness, fitness_history, average_fitness_history
    
    def construct_solutions(self, stations, drones):
        solutions = []
        num_stations = len(stations)
        
        for _ in range(self.num_ants):
            solution = []
            available_stations = list(range(num_stations))  # Tüm istasyonları kullanılabilir olarak başlat
            random.shuffle(available_stations)  # İstasyonların sırasını karıştır
            
            for drone in drones:
                if available_stations:
                    selected_station = available_stations.pop()  # Bir istasyon seç ve kullanılanlar listesinden çıkar
                    solution.append(selected_station)
                else:
                    solution.append(-1)  # Eğer kullanılabilir istasyon kalmazsa, -1 ekle
            
            solutions.append(solution)
        
        return solutions
    
    def calculate_probabilities(self, drone, stations, available_stations):
        probabilities = []
        pheromone_sum = sum([self.pheromones[station_a][station_b] ** self.alpha * (1 / self.distance(stations[station_a], stations[station_b])) ** self.beta for station_a in available_stations for station_b in available_stations])
        
        for station_b in available_stations:
            pheromone_level = self.pheromones[drone][station_b] ** self.alpha
            heuristic_value = (1 / self.distance(stations[drone], stations[station_b])) ** self.beta
            probabilities.append((pheromone_level * heuristic_value) / pheromone_sum)
        
        return probabilities
    
    def select_station(self, probabilities):
        return random.choices(range(len(probabilities)), weights=probabilities, k=1)[0]
    
    def update_pheromones(self, solutions):
        for i in range(len(self.pheromones)):
            for j in range(len(self.pheromones[i])):
                self.pheromones[i][j] *= (1 - self.evaporation_rate)
        
        for solution in solutions:
            for i in range(len(solution) - 1):
                station_a = solution[i]
                station_b = solution[i + 1]
                self.pheromones[station_a][station_b] += self.pheromone_deposit
    
    def get_best_solution(self, solutions, stations):
        best_fitness = float('inf')
        best_solution = None
        for solution in solutions:
            fitness = self.calculate_fitness(solution, stations)
            if fitness < best_fitness:
                best_fitness = fitness
                best_solution = solution
        return best_solution, best_fitness
    
    def calculate_fitness(self, solution, stations):
        total_distance = 0
        for i in range(len(solution) - 1):
            total_distance += self.distance(stations[solution[i]], stations[solution[i + 1]])
        return total_distance
    
    def distance(self, station_a, station_b):
        return math.sqrt((station_a.x - station_b.x) ** 2 + (station_a.y - station_b.y) ** 2)
