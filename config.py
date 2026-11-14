"""
Configuration and Hyperparameters
Based on research paper:
'A hybrid RL-GA-LSTM-AE framework for energy-aware and SLA-driven task scheduling in cloud computing environments'
(Scientific Reports, 2026)
"""

import os

# Base paths
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
RESULTS_DIR = os.path.join(PROJECT_ROOT, "results")
MODELS_DIR = os.path.join(PROJECT_ROOT, "saved_models")

os.makedirs(RESULTS_DIR, exist_ok=True)
os.makedirs(MODELS_DIR, exist_ok=True)

# VM Specifications (Heterogeneous Cloud Datacenter Pool)
# Table 10 & 16: 10 Heterogeneous VMs (scalable to 20 for large workloads)
VM_PROFILES = [
    {"id": 0, "name": "c5.large",    "mips": 2500, "ram": 4096,  "p_idle": 90.0,  "p_max": 210.0, "bandwidth": 1000},
    {"id": 1, "name": "c5.xlarge",   "mips": 5000, "ram": 8192,  "p_idle": 120.0, "p_max": 310.0, "bandwidth": 2000},
    {"id": 2, "name": "m5.large",    "mips": 2200, "ram": 8192,  "p_idle": 85.0,  "p_max": 195.0, "bandwidth": 1000},
    {"id": 3, "name": "m5.xlarge",   "mips": 4400, "ram": 16384, "p_idle": 110.0, "p_max": 285.0, "bandwidth": 2000},
    {"id": 4, "name": "r5.large",    "mips": 2000, "ram": 16384, "p_idle": 95.0,  "p_max": 220.0, "bandwidth": 1000},
    {"id": 5, "name": "t3.medium",   "mips": 1500, "ram": 4096,  "p_idle": 60.0,  "p_max": 140.0, "bandwidth": 500},
    {"id": 6, "name": "t3.large",    "mips": 2800, "ram": 8192,  "p_idle": 80.0,  "p_max": 180.0, "bandwidth": 1000},
    {"id": 7, "name": "c5.2xlarge",  "mips": 7500, "ram": 16384, "p_idle": 160.0, "p_max": 420.0, "bandwidth": 2500},
    {"id": 8, "name": "m5.2xlarge",  "mips": 6600, "ram": 32768, "p_idle": 150.0, "p_max": 390.0, "bandwidth": 2500},
    {"id": 9, "name": "g4dn.xlarge", "mips": 8000, "ram": 16384, "p_idle": 180.0, "p_max": 480.0, "bandwidth": 3000},
]

# Task Generation Settings (Poisson arrival, Google Cluster & RUBiS distribution)
TASK_CONFIG = {
    "arrival_rate": 5.0,        # Poisson lambda = 5
    "min_mi": 5000,             # Min instructions (MI)
    "max_mi": 80000,            # Max instructions (MI)
    "min_ram": 512,             # MB
    "max_ram": 8192,            # MB
    "priority_distribution": [0.25, 0.50, 0.25], # P1 (High), P2 (Med), P3 (Low)
    "deadline_slack_p1": 1.25,  # Tight deadline multiplier for P1
    "deadline_slack_p2": 1.75,  # Moderate deadline multiplier for P2
    "deadline_slack_p3": 2.50,  # Loose deadline multiplier for P3
}

# LSTM Workload Predictor & Autoencoder Settings (Table 14)
LSTM_CONFIG = {
    "window_size": 30,          # Sliding time window tau = 30 steps
    "input_features": 3,        # CPU load, memory usage, task arrival count
    "lstm_units_1": 64,         # Layer 1
    "lstm_units_2": 32,         # Layer 2
    "latent_dim": 16,           # Latent dimension for AE
    "learning_rate": 0.001,     # Adam lr
    "batch_size": 64,
    "epochs": 40,
    "anomaly_k": 2.0,           # Threshold factor k in tau = mu + k*sigma
}

# Genetic Algorithm Settings (Table 14)
GA_CONFIG = {
    "population_size": 50,
    "crossover_rate": 0.8,
    "mutation_rate": 0.05,
    "elite_ratio": 0.2,         # Top 20% elite chromosomes
    "generations": 30,
    "weights": [0.4, 0.35, 0.25] # Makespan, SLA, Energy
}

# Reinforcement Learning Settings (DQN / Q-Learning) (Table 14)
RL_CONFIG = {
    "learning_rate": 0.001,     # alpha
    "discount_factor": 0.95,    # gamma
    "epsilon": 0.1,             # epsilon-greedy
    "replay_buffer_size": 25000,
    "batch_size": 64,
    "weights": {                # Reward weights: w1(1-SLAv) + w2(CPU_util) - w3(Energy)
        "w1_sla": 0.45,
        "w2_cpu": 0.25,
        "w3_energy": 0.30
    }
}

# Dynamic Scaling & Provisioning Parameters
PROVISIONING_CONFIG = {
    "cooldown_period": 5,       # Steps to prevent flapping
    "safety_margin": 1.15,      # 15% headroom above predicted workload
    "emergency_reserve_vms": 2, # Reserve VMs activated on AE anomaly alert
}
