
# 📡 Ground Station Optimization and Performance Analysis for Drone Networks

<div align="center">
  <img src="https://img.shields.io/badge/Language-Python-blue?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Optimization%20Algorithms-7-lightgreen?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Scenarios-3-orange?style=for-the-badge"/>
</div>

## 🌍 Languages

- 🇹🇷 [Türkçe Açıklama](#türkçe-açıklama)
- 🇬🇧 [English Description](#english-description)

---

## 🇹🇷 Türkçe Açıklama

### 🎯 Proje Amacı

Bu proje, drone’ların en uygun yer istasyonlarına enerji verimliliği esasına göre atanmasını hedeflemektedir. Sabit ve hareketli drone/istasyon senaryolarında çeşitli optimizasyon algoritmaları uygulanarak en uygun eşleşmeler analiz edilmiştir.

### 🧪 Kullanılan Optimizasyon Algoritmaları

- 🐝 Yapay Arı Koloni Algoritması (ABC)
- 🧬 Genetik Algoritma (GA)
- 🐺 Gri Kurt Optimizasyonu (GWO)
- 🐜 Karınca Kolonisi Optimizasyonu (ACO)
- 🌪 Parçacık Sürü Optimizasyonu (PSO)
- 🦗 Çekirge Optimizasyonu (GOA)
- 🧠 Diferansiyel Gelişim Algoritması (DEA)

### 📘 Senaryolar

1. **Sabit Drone – Sabit İstasyon**  
2. **Hareketli Drone – Sabit İstasyon**  
3. **Hareketli Drone – Hareketli İstasyon**

Tüm senaryolarda algoritmaların enerji tüketimi ve uygunluk değerleri karşılaştırılmıştır.

### 📊 Değerlendirme Metrikleri

- 🔋 Enerji Tüketimi
- 📶 Sinyal Gücü Kaybı
- 🕒 Algoritma Çalışma Süresi
- 📈 Ortalama ve Standart Sapmalar
- ✅ Uygunluk Fonksiyonu Değerleri

### 🗂️ Proje Yapısı

```bash
Ground-Station-Optimization/
│
├── scenarios/
│   ├── scenario1_static.py
│   ├── scenario2_moving_drone.py
│   └── scenario3_moving_all.py
│
├── algorithms/
│   ├── pso.py
│   ├── gwo.py
│   └── ...
│
├── results/
│   └── graphs/
│
└── README.md
```

### 🚀 Nasıl Çalıştırılır?

```bash
pip install -r requirements.txt
python scenarios/scenario1_static.py
```

### 👨‍💻 Geliştiriciler

- Zeynep Sıla Kaymak  
- Can Yılmaz  
- Cenkay Kucur  
📍 Ondokuz Mayıs Üniversitesi – Bilgisayar Mühendisliği

---

## 🇬🇧 English Description

### 🎯 Project Goal

This project aims to optimize drone-to-ground station assignments based on energy efficiency. The goal is to minimize energy consumption by using optimization algorithms under various drone and station mobility scenarios.

### 🧪 Applied Optimization Algorithms

- 🐝 Artificial Bee Colony (ABC)
- 🧬 Genetic Algorithm (GA)
- 🐺 Grey Wolf Optimizer (GWO)
- 🐜 Ant Colony Optimization (ACO)
- 🌪 Particle Swarm Optimization (PSO)
- 🦗 Grasshopper Optimization Algorithm (GOA)
- 🧠 Differential Evolution Algorithm (DEA)

### 📘 Scenarios

1. **Static Drone – Static Station**  
2. **Moving Drone – Static Station**  
3. **Moving Drone – Moving Station**

All scenarios evaluate algorithm performance through fitness and energy metrics.

### 📊 Evaluation Metrics

- 🔋 Energy Consumption
- 📶 Signal Loss (Path Loss)
- 🕒 Execution Time
- 📈 Mean and Standard Deviation
- ✅ Fitness Function Results

### 🗂️ Project Structure

```bash
Ground-Station-Optimization/
│
├── scenarios/
│   ├── scenario1_static.py
│   ├── scenario2_moving_drone.py
│   └── scenario3_moving_all.py
│
├── algorithms/
│   ├── pso.py
│   ├── gwo.py
│   └── ...
│
├── results/
│   └── graphs/
│
└── README.md
```

### 🚀 How to Run

```bash
pip install -r requirements.txt
python scenarios/scenario1_static.py
```

### 👨‍💻 Contributors

- Zeynep Sıla Kaymak  
- Can Yılmaz  
- Cenkay Kucur  
📍 Ondokuz Mayıs University – Computer Engineering Department

---
