import random
import math
import time
import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from tkinter import ttk, messagebox
from pso import PSO
from grey import GreyWolfOptimizer
from aco import AntColonyOptimization
from genetic import GeneticAlgorithm
from abcalgorithm import ABC
from çekirge import GOA
from diferansiyel import DEA




class Station:
    def __init__(self, name, x, y, coverage_radius):
        self.name = name
        self.x = x
        self.y = y
        self.coverage_radius = coverage_radius
        self.area = (x - coverage_radius, y - coverage_radius, x + coverage_radius, y + coverage_radius)

    def is_inside_coverage_area(self, drone_x, drone_y):
        return (self.area[0] <= drone_x <= self.area[2]) and (self.area[1] <= drone_y <= self.area[3])
# Sabit istasyonların konumları ve özellikleri
station_positions = [
    ("İstasyon A", (200, 200)),
    ("İstasyon B", (500, 200)),
    ("İstasyon C", (200, 500)),
    ("İstasyon D", (500, 500)),
    ("İstasyon E", (350, 350))
]


class Drone:
    def __init__(self, model, max_speed, max_battery_level, x, y):
        self.model = model
        self.max_speed = max_speed
        self.max_battery_level = max_battery_level
        self.battery_level = max_battery_level
        self.x = x
        self.y = y

    def update_battery_level(self, distance):
        self.battery_level -= distance

    def is_battery_empty(self):
        return self.battery_level <= 0


def generate_drones(drone_positions):
    drones = []
    drone_models = [
        {"name": "DJI Mavic Air 2", "motor_power_per_propeller": 50, "num_propellers": 7, "processor_power": 10,
         "battery_power": 15, "sensor_power": 5, "communication_power": 3, "max_speed": 68, "max_altitude": 5000,
         "battery_capacity_mAh": 3500, "battery_voltage_V": 11.55, "battery_energy_Wh": 40.42},
        {"name": "Parrot Anafi", "motor_power_per_propeller": 50, "num_propellers": 4, "processor_power": 8,
         "battery_power": 12, "sensor_power": 4, "communication_power": 2, "max_speed": 55, "max_altitude": 4500,
         "battery_capacity_mAh": 6800, "battery_voltage_V": 11.55, "battery_energy_Wh": 78.6},
        {"name": "Skydio 2", "motor_power_per_propeller": 45, "num_propellers": 4, "processor_power": 7,
         "battery_power": 10, "sensor_power": 3, "communication_power": 2, "max_speed": 55, "max_altitude": 4500,
         "battery_capacity_mAh": 4280, "battery_voltage_V": 13.05, "battery_energy_Wh": 48.79},
        {"name": "DJI Phantom 4 Pro", "motor_power_per_propeller": 60, "num_propellers": 4, "processor_power": 10,
         "battery_power": 15, "sensor_power": 5, "communication_power": 3, "max_speed": 72, "max_altitude": 4500,
         "battery_capacity_mAh": 5870, "battery_voltage_V": 15.2, "battery_energy_Wh": 89.8},
        {"name": "Autel Robotics EVO 2", "motor_power_per_propeller": 55, "num_propellers": 4, "processor_power": 9,
         "battery_power": 13, "sensor_power": 5, "communication_power": 3, "max_speed": 72, "max_altitude": 4500,
         "battery_capacity_mAh": 7100, "battery_voltage_V": 11.55, "battery_energy_Wh": 82},
        {"name": "Yuunec Typhoon H Pro", "motor_power_per_propeller": 70, "num_propellers": 6,
         "processor_power": 12, "battery_power": 18, "sensor_power": 6, "communication_power": 4, "max_speed": 70,
         "max_altitude": 4500, "battery_capacity_mAh": 5400, "battery_voltage_V": 14.8, "battery_energy_Wh": 79.92}
    ]

    model_index = 0  # Dron modeli listesindeki indeks
    for position in drone_positions:
        x, y = position
        model_data = drone_models[model_index % len(drone_models)]  # Dron modelini sırayla al
        model_index += 1
        model = model_data["name"]
        max_speed = model_data["max_speed"]
        max_battery_level = model_data["battery_capacity_mAh"] * model_data["battery_voltage_V"] / 1000
        drone = Drone(model, max_speed, max_battery_level, x, y)
        drones.append(drone)

    return drones


def generate_random_drone_positions(num_drones):
    drone_positions = []
    drone_velocities = []
    for _ in range(num_drones):
        x = random.randint(0, 800)
        y = random.randint(0, 600)
        dx = random.uniform(-5, 5)
        dy = random.uniform(-5, 5)
        drone_positions.append((x, y))
        drone_velocities.append((dx, dy))
    return drone_positions, drone_velocities

def update_drone_positions(drone_positions, drone_velocities, time_step=1):
    new_positions = []
    for (x, y), (dx, dy) in zip(drone_positions, drone_velocities):
        new_x = x + dx * time_step
        new_y = y + dy * time_step
        new_x = max(0, min(800, new_x))  # Alan sınırlarını kontrol et
        new_y = max(0, min(600, new_y))  # Alan sınırlarını kontrol et
        new_positions.append((new_x, new_y))
    return new_positions

def check_and_resolve_collisions(drone_positions):
    new_positions = []
    occupied_positions = set()
    for pos in drone_positions:
        if pos in occupied_positions:
            # Çakışma tespit edildi, pozisyonu hafifçe ayarla
            offset_x = random.uniform(-1, 1)
            offset_y = random.uniform(-1, 1)
            new_x = pos[0] + offset_x
            new_y = pos[1] + offset_y
            new_positions.append((new_x, new_y))
        else:
            new_positions.append(pos)
        occupied_positions.add(pos)
    return new_positions

def save_results_to_file(filename, results):
    with open(filename, 'a') as f:  # 'a' mode for appending
        f.write(results)



def generate_stations(station_positions, coverage_radius):
    stations = []
    for name, (x, y) in station_positions:
        stations.append(Station(name, x, y, coverage_radius))
    return stations


# Kapsama alanı yarıçapı
coverage_radius = 50

# Alan boyutu
area_size = 500

def optimize_algorithm():
    def visualize_solution(stations, drones, best_solution, title):
        plt.figure(figsize=(8, 6))
        colors = ['blue', 'green', 'orange', 'purple', 'cyan']

        for i, station in enumerate(stations):
            color = colors[i % len(colors)]
            plt.scatter(station.x, station.y, marker='s', s=100, color=color, label=station.name)

        for i, solution in enumerate(best_solution):
            station_index, _ = solution
            station_index = int(station_index)

            if station_index == -1:
                print(f"Drone {i} hiçbir istasyona atanmadı.")
            else:
                station = stations[station_index]
                drone_pos = drones[i]
                plt.arrow(drone_pos.x, drone_pos.y, station.x - drone_pos.x, station.y - drone_pos.y,
                          head_width=0.5, head_length=0.5, fc='blue', ec='blue')
                plt.plot(drone_pos.x, drone_pos.y, marker='o', markersize=10, label=f'Drone {i}')

        plt.title(title)
        plt.xlabel('X Koordinatı')
        plt.ylabel('Y Koordinatı')
        plt.grid(True)
        plt.legend()
        plt.show()
    
    def visualize_solution2(stations, drones, best_solution_aco, title):
        plt.figure(figsize=(8, 6))
        
        # Renk paleti oluştur
        colors = ['blue', 'green', 'orange', 'purple', 'cyan']  # İstediğiniz kadar renk ekleyebilirsiniz
        
        # Istasyonları göster
        for i, station in enumerate(stations):
            color = colors[i % len(colors)]  # Renkler döngüsel olarak atanır
            plt.scatter(station.x, station.y, marker='s', s=100, color=color, label=station.name)

        # Her drone ve atandığı istasyonu göster
        for i, station_index in enumerate(best_solution_aco):
            if station_index == -1:
                print(f"Drone {i} hiçbir istasyona atanmadı.")
            else:
                station = stations[station_index]
                # Drone pozisyonu
                drone_pos = drones[i]
                # Ok çizimi
                plt.arrow(drone_pos.x, drone_pos.y, station.x - drone_pos.x, station.y - drone_pos.y,
                        head_width=0.5, head_length=0.5, fc='blue', ec='blue')
                # Drone pozisyonu
                plt.plot(drone_pos.x, drone_pos.y, marker='o', markersize=10, label=f'Drone {i}')

        plt.title(title)
        plt.xlabel('X Koordinatı')
        plt.ylabel('Y Koordinatı')
        plt.grid(True)
        plt.legend()
        plt.show()
        
    
    coverage_radius = 100

    drone_positions, _ = generate_random_drone_positions(6)  # Sadece drone_positions listesini alın
    drones = generate_drones(drone_positions)  # generate_drones fonksiyonuna sadece drone_positions listesini geçirin
    stations = generate_stations(station_positions, coverage_radius)

    total_time = 5
    time_step = 1

    
    algorithm_choice = algorithm_var.get()
    max_iterations = 10000
    fitness_values = []

    if algorithm_choice == '1':
        max_iterations = 10000
        num_particles = len(drones)
        inertia_weight = 0.8
        cognitive_weight = 1.5
        social_weight = 2.0

        start_time = time.time()

        pso = PSO(num_particles, max_iterations, inertia_weight, cognitive_weight, social_weight)
        best_solution, best_fitness, fitness_values, elapsed_time = pso.optimize(stations, drones)

        convergence_speed = max_iterations / elapsed_time

        total_distance = 0
        total_battery_usage = 0

 # Ortalama mesafe ve batarya kullanımı hesaplanması
        total_distance = sum([math.sqrt((drone.x - stations[int(station_index)].x) ** 2 + (drone.y - stations[int(station_index)].y) ** 2) 
                            for drone, (station_index, _) in zip(drones, best_solution) if station_index != -1])
        assigned_drones = len([station_index for station_index, _ in best_solution if station_index != -1])
        average_distance = total_distance / assigned_drones if assigned_drones else 0
        
        total_battery_usage = sum([1 - battery_level / drone.max_battery_level for drone, (_, battery_level) in zip(drones, best_solution)])
        average_battery_usage = total_battery_usage / len(drones)

        plt.figure(figsize=(8, 4))
        plt.plot(range(1, len(fitness_values) + 1), fitness_values, marker='o', linestyle='-')
        plt.title('PSO ile Elde Edilen Ortalama Fitness Değerleri')
        plt.xlabel('İterasyon')
        plt.ylabel('Fitness Değeri')
        plt.grid(True)
        plt.show()

        visualize_solution(stations, drones, best_solution, 'PSO ile Elde Edilen Çözüm Yolu Haritası')

        result_text.config(state=tk.NORMAL)
        result_text.delete("1.0", tk.END)
        result_text.insert(tk.END, "PSO ile Elde Edilen En İyi Çözüm:\n")
        unassigned_drones = []
        for i, solution in enumerate(best_solution):
            station_index, _ = solution
            drone = drones[i]
            if station_index == -1:
                unassigned_drones.append(drone.model)
            else:
                station = stations[int(station_index)]
                result_text.insert(tk.END, f"{drone.model} -> {station.name}\n")
            result_text.insert(tk.END, f"{drone.model} Konum: ({drone.x}, {drone.y})\n")  # Drone konumunu ekliyoruz
        
        if unassigned_drones:
            result_text.insert(tk.END, f"\nBu dronlar hiçbir istasyona atanmadı: {', '.join(unassigned_drones)}\n")
        result_text.insert(tk.END, f"\nPSO ile Elde Edilen En İyi Uygunluk Değeri: {best_fitness}\n")
        result_text.insert(tk.END, f"\nOrtalama Mesafe: {average_distance}\n")
        result_text.insert(tk.END, f"\nOrtalama Batarya Kullanımı: {average_battery_usage}\n")
        result_text.insert(tk.END, f"\nGeçen Süre: {elapsed_time:.4f} saniye\n")
        result_text.insert(tk.END, f"\nKapanma Hızı: {convergence_speed:.2f} iterasyon/saniye\n")

        # Drone pozisyon geçmişini alalım
        position_history = []
        drone_positions, drone_velocities = generate_random_drone_positions(len(drones))
        for t in range(0, 6, 1):  # 0'dan 10'a kadar 1'er saniye aralıklarla
            position_history.append((t, drone_positions.copy()))  # Mevcut pozisyonları geçmişe ekle
            drone_positions = update_drone_positions(drone_positions, drone_velocities, 1)  # Pozisyonları güncelle

        # Geçmişi ekrana yazdıralım
        for t, snapshot in position_history:
            result_text.insert(tk.END, f"\nTime {t}:\n")
            for i, (x, y) in enumerate(snapshot):
                model_name = drones[i].model  # Dronun model adını alıyoruz
                result_text.insert(tk.END, f"Drone {model_name}: Konum: ({x:.2f}, {y:.2f})\n")

        result_text.config(state=tk.DISABLED)

        results = (
        f"\nSENARYO 2 PSO ALGORTİMASI SONUÇLARI\n"
        f"\nPSO ile Elde Edilen En İyi Uygunluk Değeri: {best_fitness}\n"
        f"\nOrtalama Mesafe: {average_distance}\n"
        f"\nOrtalama Batarya Kullanımı: {average_battery_usage}\n"
        f"\nGeçen Süre: {elapsed_time:.4f} saniye\n"
        f"\nKapanma Hızı: {convergence_speed:.2f} iterasyon/saniye\n"
        )
        filename = "PSO_results2.txt"
        save_results_to_file(filename, results)



    elif algorithm_choice == '2':
        num_wolves = len(drones)
        a = 1
        A = 2
        C = 1
        b = 1
        l = 1

        start_time = time.time()

        gwo = GreyWolfOptimizer(num_wolves, max_iterations, a, A, C, b, l)
        best_solution, best_fitness_gwo = gwo.optimize(stations, drones)

        end_time = time.time()

        elapsed_time = end_time - start_time

        total_distance = 0
        total_battery_usage = 0
        fitness_values_gwo = []
        best_fitness_gwo = float('inf')
        for iteration in range(max_iterations):
            best_solution, current_best_fitness = gwo.iterate(stations, drones)
            if current_best_fitness < best_fitness_gwo:
                best_fitness_gwo = current_best_fitness
            fitness_values_gwo.append(best_fitness_gwo)

        average_distance = total_distance / len(drones)
        average_battery_usage = total_battery_usage / len(drones)

        convergence_speed = max_iterations / elapsed_time

        # Ortalama mesafe ve batarya kullanımı hesaplanması
        total_distance = sum([math.sqrt((drone.x - stations[int(station_index)].x) ** 2 + (drone.y - stations[int(station_index)].y) ** 2) 
                            for drone, (station_index, _) in zip(drones, best_solution) if station_index != -1])
        assigned_drones = len([station_index for station_index, _ in best_solution if station_index != -1])
        average_distance = total_distance / assigned_drones if assigned_drones else 0
        
        total_battery_usage = sum([1 - battery_level / drone.max_battery_level for drone, (_, battery_level) in zip(drones, best_solution)])
        average_battery_usage = total_battery_usage / len(drones)

        plt.figure(figsize=(8, 4))
        plt.plot(range(1, 10001), fitness_values_gwo[:10000], marker='o', linestyle='-')
        plt.title('GWO ile Elde Edilen Fitness Değerleri')
        plt.xlabel('İterasyon')
        plt.ylabel('Fitness Değeri')
        plt.grid(True)
        plt.show()

        visualize_solution(stations, drones, best_solution, 'GWO ile Elde Edilen Çözüm Yolu Haritası')

        result_text.config(state=tk.NORMAL)
        result_text.delete("1.0", tk.END)
        result_text.insert(tk.END, "GWO ile Elde Edilen En İyi Çözüm:\n")
        unassigned_drones = []
        for i, solution in enumerate(best_solution):
            station_index, _ = solution
            if station_index == -1:
                unassigned_drones.append(drones[i].model)
            else:
                station = stations[int(station_index)]
                drone = drones[i]
                result_text.insert(tk.END, f"{drone.model} -> {station.name}\n")
        if unassigned_drones:
            result_text.insert(tk.END, f"\nBu dronlar hiçbir istasyona atanmadı: {', '.join(unassigned_drones)}\n")
        result_text.insert(tk.END, f"\nGWO ile Elde Edilen En İyi Uygunluk Değeri: {best_fitness_gwo}\n")
        result_text.insert(tk.END, f"\nOrtalama Mesafe: {average_distance}\n")
        result_text.insert(tk.END, f"\nOrtalama Batarya Kullanımı: {average_battery_usage}\n")
        result_text.insert(tk.END, f"\nGWO Çalışma Süresi: {elapsed_time:.4f} saniye\n")
        result_text.insert(tk.END, f"\nKapanma Hızı: {convergence_speed:.2f} iterasyon/saniye\n")
        # Drone pozisyon geçmişini alalım
        position_history = []
        drone_positions, drone_velocities = generate_random_drone_positions(len(drones))
        for t in range(0, 6, 1):  # 0'dan 10'a kadar 1'er saniye aralıklarla
            position_history.append((t, drone_positions.copy()))  # Mevcut pozisyonları geçmişe ekle
            drone_positions = update_drone_positions(drone_positions, drone_velocities, 1)  # Pozisyonları güncelle

        # Geçmişi ekrana yazdıralım
        for t, snapshot in position_history:
            result_text.insert(tk.END, f"\nTime {t}:\n")
            for i, (x, y) in enumerate(snapshot):
                model_name = drones[i].model  # Dronun model adını alıyoruz
                result_text.insert(tk.END, f"Drone {model_name}: Konum: ({x:.2f}, {y:.2f})\n")

        result_text.config(state=tk.DISABLED)

        results = (
        f"\nSENARYO 2 GWO ALGORTİMASI SONUÇLARI\n"
        f"\nGWO ile Elde Edilen En İyi Uygunluk Değeri: {best_fitness_gwo}\n"
        f"\nOrtalama Mesafe: {average_distance}\n"
        f"\nOrtalama Batarya Kullanımı: {average_battery_usage}\n"
        f"\nGeçen Süre: {elapsed_time:.4f} saniye\n"
        f"\nKapanma Hızı: {convergence_speed:.2f} iterasyon/saniye\n"
        )
        filename = "GWO_results2.txt"
        save_results_to_file(filename, results)


    if algorithm_choice == '3':
        # ACO parametrelerini ayarla
        num_ants = len(drones)  # Karınca sayısı drone sayısına eşit olacak
        evaporation_rate = 0.5
        alpha = 1
        beta = 2
        pheromone_deposit = 1
        initial_pheromone = 1

        start_time = time.time()

        # ACO algoritmasını başlat ve en iyi çözümü, uygunluk geçmişini al
        aco = AntColonyOptimization(num_ants, 10000, evaporation_rate, alpha, beta, pheromone_deposit, initial_pheromone)
        best_solution, best_fitness_aco, fitness_history_aco, average_fitness_history = aco.optimize(stations, drones)

        end_time = time.time()

        elapsed_time = end_time - start_time
        total_distance = 0
        total_battery_usage = 0
        convergence_speed = 10000 / elapsed_time 

        # Ortalama mesafe hesapla
        total_distance = sum([math.sqrt((drone.x - stations[int(station_index)].x) ** 2 + (drone.y - stations[int(station_index)].y) ** 2) 
                    for drone, station_index in zip(drones, best_solution) if station_index != -1])

        assigned_drones = len([station_index for station_index in best_solution if station_index != -1])
        average_distance = total_distance / assigned_drones if assigned_drones > 0 else 0

        # Ortalama batarya kullanımı hesapla
        total_battery_usage = sum([1 - battery_level / drone.max_battery_level 
                                for drone, battery_level in zip(drones, best_solution) 
                                if battery_level != -1])
        average_battery_usage = total_battery_usage / len(drones)

        # ACO'nun her iterasyonundaki ortalama uygunluk değerlerini görselleştir
        plt.figure(figsize=(8, 4))
        plt.plot(range(1, len(average_fitness_history) + 1), average_fitness_history, marker='o', linestyle='-')
        plt.title('ACO ile Elde Edilen Ortalama Fitness Değerleri')
        plt.xlabel('İterasyon')
        plt.ylabel('Ortalama Fitness Değeri')
        plt.grid(True)
        plt.show()

        # Çözümü görselleştir
        visualize_solution2(stations, drones, best_solution, 'ACO ile Elde Edilen Çözüm Yolu Haritası')

        # Sonuçları hazırla
        result_text.config(state=tk.NORMAL)
        result_text.delete("1.0", tk.END)
        result_text.insert(tk.END, "ACO ile Elde Edilen En İyi Çözüm:\n\n")
        
        unassigned_drones = []
        for i, solution_index in enumerate(best_solution):
            if solution_index == -1:
                unassigned_drones.append(drones[i].model)
            else:
                station = stations[solution_index]
                drone = drones[i]
                result_text.insert(tk.END, f"{drone.model} -> {station.name}\n")
        
        if unassigned_drones:
            result_text.insert(tk.END, f"\nBu dronlar hiçbir istasyona atanmadı: {', '.join(unassigned_drones)}\n")
        
        result_text.insert(tk.END, f"\nACO ile Elde Edilen En İyi Uygunluk Değeri: {best_fitness_aco}\n")  # En iyi uygunluk değerini ekleyin
        result_text.insert(tk.END, f"\nOrtalama Mesafe: {average_distance}\n")
        result_text.insert(tk.END, f"\nOrtalama Batarya Kullanımı: {average_battery_usage}\n")
        result_text.insert(tk.END, f"ACO Çalışma Süresi: {elapsed_time:.4f} saniye\n")
        result_text.insert(tk.END, f"Kapanma Hızı: {convergence_speed:.2f} iterasyon/saniye\n")
        # Drone pozisyon geçmişini alalım
        position_history = []
        drone_positions, drone_velocities = generate_random_drone_positions(len(drones))
        for t in range(0, 6, 1):  # 0'dan 10'a kadar 1'er saniye aralıklarla
            position_history.append((t, drone_positions.copy()))  # Mevcut pozisyonları geçmişe ekle
            drone_positions = update_drone_positions(drone_positions, drone_velocities, 1)  # Pozisyonları güncelle

        # Geçmişi ekrana yazdıralım
        for t, snapshot in position_history:
            result_text.insert(tk.END, f"\nTime {t}:\n")
            for i, (x, y) in enumerate(snapshot):
                model_name = drones[i].model  # Dronun model adını alıyoruz
                result_text.insert(tk.END, f"Drone {model_name}: Konum: ({x:.2f}, {y:.2f})\n")

        result_text.config(state=tk.DISABLED)

        results = (
        f"\nSENARYO 2 ACO ALGORTİMASI SONUÇLARI\n"
        f"\nACO ile Elde Edilen En İyi Uygunluk Değeri: {best_fitness_aco}\n"
        f"\nOrtalama Mesafe: {average_distance}\n"
        f"\nOrtalama Batarya Kullanımı: {average_battery_usage}\n"
        f"\nGeçen Süre: {elapsed_time:.4f} saniye\n"
        f"\nKapanma Hızı: {convergence_speed:.2f} iterasyon/saniye\n"
        )
        filename = "ACO_results2.txt"
        save_results_to_file(filename, results)
    
    elif algorithm_choice == '4':
        
        # Genetik Algoritma Parametreleri
        population_size = len(drones)
        mutation_rate = 0.01
        crossover_rate = 0.7
        max_generations = 10000

        start_time = time.time()

        # Genetik Algoritmayı çalıştır
        ga = GeneticAlgorithm(population_size, mutation_rate, crossover_rate, max_generations)
        best_solution, best_fitness, fitness_history = ga.optimize(drones, stations)

        end_time = time.time()
        elapsed_time = end_time - start_time

        total_distance = 0
        total_battery_usage = 0
        fitness_values = []

        # Ortalama mesafe ve batarya kullanımı hesaplanması
        total_distance = sum([math.sqrt((drone.x - stations[int(station_index)].x) ** 2 + (drone.y - stations[int(station_index)].y) ** 2) 
                            for drone, (station_index, _) in zip(drones, best_solution) if station_index != -1])
        assigned_drones = len([station_index for station_index, _ in best_solution if station_index != -1])
        average_distance = total_distance / assigned_drones if assigned_drones else 0
        
        total_battery_usage = sum([1 - battery_level / drone.max_battery_level for drone, (_, battery_level) in zip(drones, best_solution)])
        average_battery_usage = total_battery_usage / len(drones)
        convergence_speed = max_generations / elapsed_time

        # Sonuçları görselleştirme
        plt.plot(fitness_history)
        plt.xlabel('İterasyon')
        plt.ylabel('Fitness Değeri')
        plt.title('Genetik Algoritma ile Elde Edilen Fitness Değerleri')
        plt.show()

        # Çözümü görselleştir
        visualize_solution(stations, drones, best_solution, 'Genetik Algoritma ile Elde Edilen Çözüm Yolu Haritası')

        # Sonuçları ekrana yazdır
        result_text.config(state=tk.NORMAL)
        result_text.delete("1.0", tk.END)
        result_text.insert(tk.END, "Genetik Algoritma ile Elde Edilen En İyi Çözüm:\n")
        unassigned_drones = []
        for i, solution in enumerate(best_solution):
            station_index, _ = solution
            if station_index == -1:
                unassigned_drones.append(drones[i].model)
            else:
                station = stations[int(station_index)]
                drone = drones[i]
                result_text.insert(tk.END, f"{drone.model} -> {station.name}\n")
        if unassigned_drones:
            result_text.insert(tk.END, f"\nBu dronlar hiçbir istasyona atanmadı: {', '.join(unassigned_drones)}\n")
        result_text.insert(tk.END, f"\nGenetik Algoritma ile Elde Edilen En İyi Uygunluk Değeri: {best_fitness}\n")
        result_text.insert(tk.END, f"\nOrtalama Mesafe: {average_distance}\n")
        result_text.insert(tk.END, f"\nOrtalama Batarya Kullanımı: {average_battery_usage}\n")
        result_text.insert(tk.END, f"\nÇalışma Süresi: {elapsed_time:.4f} saniye\n")
        result_text.insert(tk.END, f"\nKapanma Hızı: {convergence_speed:.2f} iterasyon/saniye\n")
        # Drone pozisyon geçmişini alalım
        position_history = []
        drone_positions, drone_velocities = generate_random_drone_positions(len(drones))
        for t in range(0, 6, 1):  # 0'dan 10'a kadar 1'er saniye aralıklarla
            position_history.append((t, drone_positions.copy()))  # Mevcut pozisyonları geçmişe ekle
            drone_positions = update_drone_positions(drone_positions, drone_velocities, 1)  # Pozisyonları güncelle

        # Geçmişi ekrana yazdıralım
        for t, snapshot in position_history:
            result_text.insert(tk.END, f"\nTime {t}:\n")
            for i, (x, y) in enumerate(snapshot):
                model_name = drones[i].model  # Dronun model adını alıyoruz
                result_text.insert(tk.END, f"Drone {model_name}: Konum: ({x:.2f}, {y:.2f})\n")

        result_text.config(state=tk.DISABLED)
        results = (
        f"\nSENARYO 2 GA ALGORTİMASI SONUÇLARI\n"
        f"\nGA ile Elde Edilen En İyi Uygunluk Değeri: {best_fitness}\n"
        f"\nOrtalama Mesafe: {average_distance}\n"
        f"\nOrtalama Batarya Kullanımı: {average_battery_usage}\n"
        f"\nGeçen Süre: {elapsed_time:.4f} saniye\n"
        f"\nKapanma Hızı: {convergence_speed:.2f} iterasyon/saniye\n"
        )
        filename = "GA_results2.txt"
        save_results_to_file(filename, results)

    elif algorithm_choice == '5':
        population_size = len(drones)
        limit = 100
        max_iterations = 10000
        num_onlooker_bees = population_size // 2  # Employed bees ve onlooker bees toplam nüfusun yarısı
        num_employed_bees = population_size - num_onlooker_bees  # Diğer yarısı employed bees olacak

        start_time = time.time()

        abc = ABC(num_employed_bees, num_onlooker_bees, max_iterations, limit, stations, drones)
        best_solution, best_fitness, fitness_values = abc.optimize()  # fitness_values'i de al

        end_time = time.time()
        elapsed_time = end_time - start_time
        # Ortalama mesafe ve batarya kullanımı hesaplanması
        total_distance = sum([math.sqrt((drone.x - stations[int(station_index)].x) ** 2 + (drone.y - stations[int(station_index)].y) ** 2) 
                            for drone, (station_index, _) in zip(drones, best_solution) if station_index != -1])
        assigned_drones = len([station_index for station_index, _ in best_solution if station_index != -1])
        average_distance = total_distance / assigned_drones if assigned_drones else 0
        
        total_battery_usage = sum([1 - battery_level / drone.max_battery_level for drone, (_, battery_level) in zip(drones, best_solution)])
        average_battery_usage = total_battery_usage / len(drones)
        convergence_speed = max_iterations / elapsed_time
        # Grafiği çizmek için bir fonksiyon ekleyin
        def plot_fitness_values(fitness_values):
            plt.plot(range(len(fitness_values)), fitness_values, 'b-')
            plt.xlabel('Iteration')
            plt.ylabel('Fitness Değeri')
            plt.title('ABC Algoritması ile Elde Edilen Fitness Değerleri')
            plt.show()

        # Fitness değerlerini grafiğe dök
        plot_fitness_values(fitness_values)

        # Çözüm yolunu görselleştir
        visualize_solution(stations, drones, best_solution, 'ABC Algoritması ile Elde Edilen Çözüm Yolu Haritası')

        # Sonuçları ekrana yazdır
        result_text.config(state=tk.NORMAL)
        result_text.delete("1.0", tk.END)
        result_text.insert(tk.END, "ABC Algoritması ile Elde Edilen En İyi Çözüm:\n")
        unassigned_drones = []
        for i, solution in enumerate(best_solution):
            station_index, _ = solution
            if station_index == -1:
                unassigned_drones.append(drones[i].model)
            else:
                station = stations[int(station_index)]
                drone = drones[i]
                result_text.insert(tk.END, f"{drone.model} -> {station.name}\n")

        if unassigned_drones:
            result_text.insert(tk.END, f"\nBu dronlar hiçbir istasyona atanmadı: {', '.join(unassigned_drones)}\n")

        result_text.insert(tk.END, f"\nABC Algoritması ile Elde Edilen En İyi Uygunluk Değeri: {best_fitness}\n")
        result_text.insert(tk.END, f"\nOrtalama Mesafe: {average_distance}\n")
        result_text.insert(tk.END, f"\nOrtalama Batarya Kullanımı: {average_battery_usage}\n")
        result_text.insert(tk.END, f"\nÇalışma Süresi: {elapsed_time:.4f} saniye\n")
        result_text.insert(tk.END, f"\nKapanma Hızı: {convergence_speed:.2f} iterasyon/saniye\n")

        # Drone pozisyon geçmişini alalım ve ekrana yazdıralım
        position_history = []
        drone_positions, drone_velocities = generate_random_drone_positions(len(drones))
        for t in range(0, 6, 1):  # 0'dan 10'a kadar 1'er saniye aralıklarla
            position_history.append((t, drone_positions.copy()))  # Mevcut pozisyonları geçmişe ekle
            drone_positions = update_drone_positions(drone_positions, drone_velocities, 1)  # Pozisyonları güncelle

        for t, snapshot in position_history:
            result_text.insert(tk.END, f"\nTime {t}:\n")
            for i, (x, y) in enumerate(snapshot):
                model_name = drones[i].model  # Dronun model adını alıyoruz
                result_text.insert(tk.END, f"Drone {model_name}: Konum: ({x:.2f}, {y:.2f})\n")

        result_text.config(state=tk.DISABLED)
        results = (
        f"\nSENARYO 2 ABC ALGORTİMASI SONUÇLARI\n"
        f"\nABC ile Elde Edilen En İyi Uygunluk Değeri: {best_fitness}\n"
        f"\nOrtalama Mesafe: {average_distance}\n"
        f"\nOrtalama Batarya Kullanımı: {average_battery_usage}\n"
        f"\nGeçen Süre: {elapsed_time:.4f} saniye\n"
        f"\nKapanma Hızı: {convergence_speed:.2f} iterasyon/saniye\n"
        )
        filename = "ABC_results2.txt"
        save_results_to_file(filename, results)

    elif algorithm_choice == '6':
        population_size = len(drones)
        max_iterations = 10000

        start_time = time.time()

        goa = GOA(population_size, max_iterations=10000)
        best_solution, best_fitness, fitness_history,all_fitness_values,avg_fitness_history, unassigned_drones = goa.optimize(drones, stations)

        end_time = time.time()
        elapsed_time = end_time - start_time

        total_distance = 0
        total_battery_usage = 0

        # Ortalama mesafe ve batarya kullanımı hesaplanması
        total_distance = sum([math.sqrt((drone.x - stations[int(station_index)].x) ** 2 + (drone.y - stations[int(station_index)].y) ** 2) 
                            for drone, (station_index, _) in zip(drones, best_solution) if station_index != -1])
        assigned_drones = len([station_index for station_index, _ in best_solution if station_index != -1])
        average_distance = total_distance / assigned_drones if assigned_drones else 0
        
        total_battery_usage = sum([1 - battery_level / drone.max_battery_level for drone, (_, battery_level) in zip(drones, best_solution)])
        average_battery_usage = total_battery_usage / len(drones)
        convergence_speed = max_iterations / elapsed_time

        # Plot the fitness history
        plt.figure(figsize=(10, 6))
        plt.plot(avg_fitness_history, label='Average Fitness', color='blue', linewidth=2)
        plt.plot(fitness_history, label='Best Fitness', color='black', linewidth=2)
        plt.xlabel('Iterations')
        plt.ylabel('Fitness')
        plt.title('GOA Fitness Convergence')
        plt.legend()
        plt.grid(True)
        plt.show()


        # Çözümü görselleştir
        visualize_solution(stations, drones, best_solution, 'Çekirge Optimizasyon Algoritması ile Elde Edilen Çözüm Yolu Haritası')

        # Sonuçları ekrana yazdır
        result_text.config(state=tk.NORMAL)
        result_text.delete("1.0", tk.END)
        result_text.insert(tk.END, "Çekirge Optimizasyon Algoritması ile Elde Edilen En İyi Çözüm:\n")
        for i, solution in enumerate(best_solution):
            station_index, _ = solution
            if station_index == -1:
                unassigned_drones.append(drones[i].model)
            else:
                station = stations[int(station_index)]
                drone = drones[i]
                result_text.insert(tk.END, f"{drone.model} -> {station.name}\n")
        if unassigned_drones:
            unassigned_drones_str = [str(drone) for drone in unassigned_drones]
            result_text.insert(tk.END, f"\nBu dronlar hiçbir istasyona atanmadı: {', '.join(unassigned_drones_str)}\n")
        result_text.insert(tk.END, f"\nÇekirge Optimizasyon Algoritması ile Elde Edilen En İyi Uygunluk Değeri: {best_fitness}\n")
        result_text.insert(tk.END, f"\nOrtalama Mesafe: {average_distance}\n")
        result_text.insert(tk.END, f"\nOrtalama Batarya Kullanımı: {average_battery_usage}\n")
        result_text.insert(tk.END, f"\nÇalışma Süresi: {elapsed_time:.4f} saniye\n")
        result_text.insert(tk.END, f"\nKapanma Hızı: {convergence_speed:.2f} iterasyon/saniye\n")
        # Drone pozisyon geçmişini alalım
        position_history = []
        drone_positions, drone_velocities = generate_random_drone_positions(len(drones))
        for t in range(0, 6, 1):  # 0'dan 10'a kadar 1'er saniye aralıklarla
            position_history.append((t, drone_positions.copy()))  # Mevcut pozisyonları geçmişe ekle
            drone_positions = update_drone_positions(drone_positions, drone_velocities, 1)  # Pozisyonları güncelle

        # Geçmişi ekrana yazdıralım
        for t, snapshot in position_history:
            result_text.insert(tk.END, f"\nTime {t}:\n")
            for i, (x, y) in enumerate(snapshot):
                model_name = drones[i].model  # Dronun model adını alıyoruz
                result_text.insert(tk.END, f"Drone {model_name}: Konum: ({x:.2f}, {y:.2f})\n")

        result_text.config(state=tk.DISABLED)
    
        results = (
        f"\nSENARYO 2 GOA ALGORTİMASI SONUÇLARI\n"
        f"\nGOA ile Elde Edilen En İyi Uygunluk Değeri: {best_fitness}\n"
        f"\nOrtalama Mesafe: {average_distance}\n"
        f"\nOrtalama Batarya Kullanımı: {average_battery_usage}\n"
        f"\nGeçen Süre: {elapsed_time:.4f} saniye\n"
        f"\nKapanma Hızı: {convergence_speed:.2f} iterasyon/saniye\n"
        )
        filename = "GOA_results2.txt"
        save_results_to_file(filename, results)


    elif algorithm_choice == '7':
     # DEA için gerekli parametreler
        num_particles = len(drones)
        scaling_factor = 0.8
        crossover_probability = 0.9

        # DEA'nın başlatılması ve sonuçların hesaplanması
        dea = DEA(num_particles, max_iterations, scaling_factor, crossover_probability)
        best_solution, best_fitness, fitness_values, elapsed_time = dea.optimize(stations, drones)

        # Fitness değerlerinin grafiğinin çizdirilmesi
        plt.figure(figsize=(8, 4))
        plt.plot(range(1, max_iterations + 1), fitness_values, marker='o', linestyle='-')
        plt.title('DEA ile Elde Edilen Fitness Değerleri')
        plt.xlabel('İterasyon')
        plt.ylabel('Fitness Değeri')
        plt.grid(True)
        plt.show()

        # Çözümün görselleştirilmesi
        visualize_solution(stations, drones, best_solution, 'DEA ile Elde Edilen Çözüm Yolu Haritası')

        # Ortalama mesafe ve batarya kullanımı hesaplanması
        total_distance = sum([math.sqrt((drone.x - stations[int(station_index)].x) ** 2 + (drone.y - stations[int(station_index)].y) ** 2) 
                            for drone, (station_index, _) in zip(drones, best_solution) if station_index != -1])
        assigned_drones = len([station_index for station_index, _ in best_solution if station_index != -1])
        average_distance = total_distance / assigned_drones if assigned_drones else 0
        
        total_battery_usage = sum([1 - battery_level / drone.max_battery_level for drone, (_, battery_level) in zip(drones, best_solution)])
        average_battery_usage = total_battery_usage / len(drones)
        
        # Kapanma hızı hesaplanması
        convergence_speed = max_iterations / elapsed_time

        # Sonuçların GUI üzerinde gösterilmesi
        result_text.config(state=tk.NORMAL)
        result_text.delete("1.0", tk.END)
        result_text.insert(tk.END, "DEA ile Elde Edilen En İyi Çözüm:\n")
        unassigned_drones = []
        for i, solution in enumerate(best_solution):
            station_index, _ = solution
            if station_index == -1:
                unassigned_drones.append(drones[i].model)
            else:
                station = stations[int(station_index)]
                drone = drones[i]
                result_text.insert(tk.END, f"{drone.model} -> {station.name}\n")
        if unassigned_drones:
            result_text.insert(tk.END, f"\nBu dronlar hiçbir istasyona atanmadı: {', '.join(unassigned_drones)}\n")
        result_text.insert(tk.END, f"\nDEA ile Elde Edilen En İyi Uygunluk Değeri: {best_fitness}\n")
        result_text.insert(tk.END, f"\nOrtalama Mesafe: {average_distance}\n")
        result_text.insert(tk.END, f"\nOrtalama Batarya Kullanımı: {average_battery_usage}\n")
        result_text.insert(tk.END, f"\nGeçen Süre: {elapsed_time:.4f} saniye\n")
        result_text.insert(tk.END, f"\nKapanma Hızı: {convergence_speed:.2f} iterasyon/saniye\n")
        # Drone pozisyon geçmişini alalım
        position_history = []
        drone_positions, drone_velocities = generate_random_drone_positions(len(drones))
        for t in range(0, 6, 1):  # 0'dan 10'a kadar 1'er saniye aralıklarla
            position_history.append((t, drone_positions.copy()))  # Mevcut pozisyonları geçmişe ekle
            drone_positions = update_drone_positions(drone_positions, drone_velocities, 1)  # Pozisyonları güncelle

        # Geçmişi ekrana yazdıralım
        for t, snapshot in position_history:
            result_text.insert(tk.END, f"\nTime {t}:\n")
            for i, (x, y) in enumerate(snapshot):
                model_name = drones[i].model  # Dronun model adını alıyoruz
                result_text.insert(tk.END, f"Drone {model_name}: Konum: ({x:.2f}, {y:.2f})\n")

        result_text.config(state=tk.DISABLED)

        results = (
        f"\nSENARYO 2 DEA ALGORTİMASI SONUÇLARI\n"
        f"\nDEA ile Elde Edilen En İyi Uygunluk Değeri: {best_fitness}\n"
        f"\nOrtalama Mesafe: {average_distance}\n"
        f"\nOrtalama Batarya Kullanımı: {average_battery_usage}\n"
        f"\nGeçen Süre: {elapsed_time:.4f} saniye\n"
        f"\nKapanma Hızı: {convergence_speed:.2f} iterasyon/saniye\n"
        )
        filename = "DEA_results2.txt"
        save_results_to_file(filename, results)


# Ana arayüz
root = tk.Tk()
root.title("Drone ve İstasyon Optimizasyonu")

# Buton Stilleri
style = ttk.Style()
style.configure('TButton', font=('calibri', 10, 'bold'), foreground='black')

# Arka Plan Rengi
root.configure(bg='#282c34')


# Buton Stilleri
style = ttk.Style()
style.configure('TButton', font=('calibri', 10, 'bold'), foreground='black')

# Arka Plan Rengi
root.configure(bg='#282c34')

# Algoritma Seçim Kısmı
algorithm_frame = tk.Frame(root, bg='#282c34')
algorithm_frame.pack(pady=10)

tk.Label(algorithm_frame, text="HAREKETLİ DRONE, SABİT YER İSTASYONU", bg='#282c34', fg='#ff6347', font=('calibri', 16, 'bold')).grid(row=0, column=0, columnspan=2, pady=5)
tk.Label(algorithm_frame, text="Optimizasyon Algoritması Seçin:", bg='#282c34', fg='#ff6347', font=('calibri', 16, 'bold')).grid(row=1, column=0, columnspan=2, pady=5)


algorithm_var = tk.StringVar(value='1')

tk.Radiobutton(algorithm_frame, text="Parçacık Sürü Optimizasyonu (PSO)", variable=algorithm_var, value='1', bg='#282c34', fg='#61dafb', font=('calibri', 12)).grid(row=2, column=0, columnspan=2, padx=5, pady=2, sticky=tk.W)
tk.Radiobutton(algorithm_frame, text="Grey Wolf Optimizer (GWO)", variable=algorithm_var, value='2', bg='#282c34', fg='#61dafb', font=('calibri', 12)).grid(row=3, column=0, columnspan=2, padx=5, pady=2, sticky=tk.W)
tk.Radiobutton(algorithm_frame, text="Ant Colony Optimization (ACO)", variable=algorithm_var, value='3', bg='#282c34', fg='#61dafb', font=('calibri', 12)).grid(row=4, column=0, columnspan=2, padx=5, pady=2, sticky=tk.W)
tk.Radiobutton(algorithm_frame, text="Genetik Algoritma (GA)", variable=algorithm_var, value='4', bg='#282c34', fg='#61dafb', font=('calibri', 12)).grid(row=5, column=0, columnspan=2, padx=5, pady=2, sticky=tk.W)
tk.Radiobutton(algorithm_frame, text="Artificial Bee Colony Algorithm (ABC)", variable=algorithm_var, value='5', bg='#282c34', fg='#61dafb', font=('calibri', 12)).grid(row=6, column=0, columnspan=2, padx=5, pady=2, sticky=tk.W)
tk.Radiobutton(algorithm_frame, text="Çekirge Optimizasyon Algoritması (GOA) ", variable=algorithm_var, value='6', bg='#282c34', fg='#61dafb', font=('calibri', 12)).grid(row=7, column=0, columnspan=2, padx=5, pady=2, sticky=tk.W)
tk.Radiobutton(algorithm_frame, text="Differential Evolution Algorithm (DEA) ", variable=algorithm_var, value='7', bg='#282c34', fg='#61dafb', font=('calibri', 12)).grid(row=8, column=0, columnspan=2, padx=5, pady=2, sticky=tk.W)

# Optimize Et Butonu
tk.Button(root, text="Optimize Et", command=optimize_algorithm, bg='#4CAF50', fg='#ffffff', font=('calibri', 12, 'bold')).pack(pady=10)

# Sonuç Metni için Çerçeve
result_frame = tk.Frame(root, bg='#282c34', bd=2)
result_frame.pack(padx=10, pady=10)

tk.Label(result_frame, text="Optimizasyon Sonuçları:", bg='#282c34', fg='#ff6347', font=('calibri', 16, 'bold')).pack(pady=5)
result_text = tk.Text(result_frame, height=25, width=100, bg='#1e1e1e', fg='#ffffff', font=('calibri', 12))
result_text.pack()
result_text.config(state=tk.DISABLED)

# Ana döngüyü başlat
root.mainloop()