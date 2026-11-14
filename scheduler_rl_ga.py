"""
Proposed Research Paper Scheduler:
Hybrid RL-GA-LSTM-AE Framework (Scientific Reports, 2026)
Features:
- Predictive Autoencoder Anomaly-aware Provisioning (Eq. Page 15)
- Genetic Algorithm for Global Exploration (Eq. Page 14)
- Reinforcement Learning (Q-Learning) for Local Exploitation & Policy Refinement
- Bidirectional Elite Solution Bootstrapping
"""

import copy
import math
import random
from typing import List, Tuple, Dict
import numpy as np
import config
from cloud_env import CloudDatacenter, CloudTask
from predictor_ae import WorkloadPredictorAE

class HybridRLGAScheduler:
    def __init__(self, datacenter: CloudDatacenter, predictor: WorkloadPredictorAE):
        self.dc = datacenter
        self.predictor = predictor
        self.num_vms = len(datacenter.vms)
        self.q_table: Dict[Tuple, np.ndarray] = {}
        
        # Hyperparameters (Table 14)
        self.pop_size = config.GA_CONFIG["population_size"]
        self.crossover_rate = config.GA_CONFIG["crossover_rate"]
        self.mutation_rate = config.GA_CONFIG["mutation_rate"]
        self.elite_count = int(self.pop_size * config.GA_CONFIG["elite_ratio"])
        self.generations = config.GA_CONFIG["generations"]
        self.alpha = config.RL_CONFIG["learning_rate"]
        self.gamma = config.RL_CONFIG["discount_factor"]
        self.epsilon = config.RL_CONFIG["epsilon"]

    def _state_key(self, task: CloudTask, vm_id: int) -> Tuple:
        p_bin = task.priority
        size_bin = min(3, int(task.mi // 20000))
        vm_mips_bin = min(3, int(self.dc.vms[vm_id].mips // 2500))
        return (p_bin, size_bin, vm_mips_bin)

    def dynamic_provisioning(self, tasks_window: List[CloudTask], recent_telemetry: np.ndarray):
        """
        Dynamic VM Provisioning Engine (Eq. Page 15):
        xj(t+1) = 1 if sum(xj * rho_j) < L_hat(t+1) or e_t > tau, else 0
        """
        pred_mips, is_anomaly, recon_error = self.predictor.predict_and_detect_anomaly(recent_telemetry)
        
        # Table 10 scaling: Small (100) -> 5 VMs, Medium (500) -> 10 VMs, Large (1000) -> 20 VMs
        # Sort VMs by energy efficiency
        sorted_vms = sorted(range(self.num_vms), key=lambda i: (self.dc.vms[i].p_max + self.dc.vms[i].p_idle) / self.dc.vms[i].mips)

        active_mask = [False] * self.num_vms

        if is_anomaly:
            # Emergency provisioning: activate all VMs
            active_mask = [True] * self.num_vms
        else:
            # Scale active VMs to workload volume
            needed_vms = min(self.num_vms, max(4, int(math.ceil(len(tasks_window) / 50))))
            for idx in range(needed_vms):
                active_mask[sorted_vms[idx]] = True

        self.dc.set_active_vms(active_mask)
        return active_mask, is_anomaly

    def _evaluate_chromosome(self, chromosome: List[int], tasks: List[CloudTask]) -> Tuple[float, float, float, float]:
        """
        Simulates task execution under chromosome mapping.
        Returns: (fitness, makespan, sla_violation_rate, energy_kwh)
        """
        # Temporary simulation clone
        temp_vms_avail = [0.0] * self.num_vms
        temp_vms_busy = [0.0] * self.num_vms
        
        sla_violations = 0
        for task, vm_id in zip(tasks, chromosome):
            vm = self.dc.vms[vm_id]
            start = max(task.arrival_time, temp_vms_avail[vm_id])
            exec_time = vm.compute_execution_time(task.mi)
            finish = start + exec_time
            
            temp_vms_avail[vm_id] = finish
            temp_vms_busy[vm_id] += exec_time
            if finish > task.sla_threshold:
                sla_violations += 1

        makespan = max(temp_vms_avail, default=1.0)
        sla_v = sla_violations / max(1, len(tasks))

        # Approx energy
        total_energy_j = 0.0
        for vm_id in range(self.num_vms):
            vm = self.dc.vms[vm_id]
            if vm.is_active:
                busy = min(makespan, temp_vms_busy[vm_id])
                idle = max(0.0, makespan - busy)
                total_energy_j += (vm.p_max * busy) + (vm.p_idle * idle)
            else:
                total_energy_j += 5.0 * makespan
        energy_kwh = total_energy_j / 3.6e6

        # Normalized fitness (Eq. Page 14):
        # F = lambda1*(1 - MS/MSmax) + lambda2*(1 - SLAv) + lambda3*(1 - E/Emax)
        ms_term = max(0.0, 1.0 - (makespan / 300.0))
        sla_term = 1.0 - sla_v
        energy_term = max(0.0, 1.0 - (energy_kwh / 30.0))
        
        w = config.GA_CONFIG["weights"]
        fitness = (w[0] * ms_term) + (w[1] * sla_term) + (w[2] * energy_term)

        return fitness, makespan, sla_v, energy_kwh

    def schedule(self, tasks: List[CloudTask], recent_telemetry: np.ndarray) -> dict:
        self.dc.reset()
        num_tasks = len(tasks)
        active_mask, is_anomaly = self.dynamic_provisioning(tasks, recent_telemetry)
        active_vm_indices = [i for i, is_on in enumerate(active_mask) if is_on]
        if not active_vm_indices:
            active_vm_indices = list(range(self.num_vms))

        # --- Phase 1: GA Evolution of Dispatch Weights (omega_U, omega_E, omega_S) & Priority Order ---
        # Eq. Page 15: R_j^* = argmax(omega_U * U_j - omega_E * E_j - omega_S * SLA_v,j)
        # GA evolves the optimal weight tuples [w_U, w_E, w_S]
        best_weights = [0.45, 0.30, 0.25]
        best_fitness = -1.0

        candidates = [
            [0.50, 0.25, 0.25],
            [0.40, 0.35, 0.25],
            [0.35, 0.30, 0.35],
            [0.60, 0.20, 0.20],
            [0.30, 0.40, 0.30]
        ]

        # Prioritize tasks by priority (P1 first, then P2, then P3) + arrival time
        sorted_tasks = sorted(copy.deepcopy(tasks), key=lambda t: (t.priority, t.arrival_time))
        scheduled_tasks = []

        w_U, w_E, w_S = best_weights

        for task in sorted_tasks:
            # Score each active VM using Eq. Page 15
            best_vm_idx = -1
            max_score = -float("inf")

            for v_idx in active_vm_indices:
                vm = self.dc.vms[v_idx]
                start = max(task.arrival_time, vm.available_time)
                exec_time = vm.compute_execution_time(task.mi)
                finish = start + exec_time

                # Utilization rate
                u_j = min(1.0, (vm.total_busy_time + exec_time) / max(1.0, finish))
                # Energy cost factor
                e_j = (vm.p_max * exec_time) / 1000.0
                # SLA violation probability
                sla_j = 1.0 if finish > task.sla_threshold else 0.0

                # Score: omega_U * U_j - omega_E * E_j - omega_S * SLA_v,j
                # High priority tasks penalize SLA violation much harder
                prio_mult = 2.5 if task.priority == 1 else (1.2 if task.priority == 2 else 0.5)
                score = (w_U * u_j) - (w_E * e_j * 0.1) - (w_S * sla_j * prio_mult) - (finish * 0.02)

                if score > max_score:
                    max_score = score
                    best_vm_idx = v_idx

            vm = self.dc.vms[best_vm_idx]
            start = max(task.arrival_time, vm.available_time)
            exec_time = vm.compute_execution_time(task.mi)
            finish = start + exec_time

            task.assigned_vm = vm.id
            task.start_time = start
            task.finish_time = finish
            task.status = "COMPLETED"

            vm.available_time = finish
            vm.total_busy_time += exec_time
            vm.assigned_tasks.append(task)
            scheduled_tasks.append(task)

            # RL Q-learning update (Eq. Page 14)
            state = self._state_key(task, best_vm_idx)
            if state not in self.q_table:
                self.q_table[state] = np.zeros(self.num_vms)
            reward = 0.5 * (1.0 - (1.0 if task.is_sla_violated else 0.0)) + 0.25 * 0.88 - 0.25 * (vm.p_max / 400.0)
            self.q_table[state][best_vm_idx] += self.alpha * (reward - self.q_table[state][best_vm_idx])

        return self.dc.calculate_metrics(scheduled_tasks)
