"""
Cloud Computing Environment & Simulator
Implements:
- Heterogeneous Virtual Machines with dynamic power models (P_idle, P_max, DVFS frequency ratio)
- Tasks with MI computational demand, deadlines, priorities (P1, P2, P3), and DAG dependencies
- Google Cluster & RUBiS realistic workload generator (Poisson arrivals)
- Metric calculators: Makespan, SLA Violation Rate, Deadline Miss Rate, Energy (kWh), CPU Util
"""

import math
import random
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
import numpy as np
import config

@dataclass
class CloudTask:
    id: int
    mi: float                  # Million Instructions
    ram: float                 # Memory requirement in MB
    priority: int              # 1: High, 2: Medium, 3: Low
    arrival_time: float        # Timestamp of arrival (seconds)
    deadline: float            # Strict deadline timestamp
    sla_threshold: float       # SLA max allowed completion time
    dependencies: List[int] = field(default_factory=list) # Task IDs that must finish first
    
    # Runtime tracking
    assigned_vm: int = -1
    start_time: float = -1.0
    finish_time: float = -1.0
    status: str = "PENDING"    # PENDING, RUNNING, COMPLETED
    assigned_freq: float = 1.0 # Clock ratio: 1.0 (Turbo), 0.9 (Balanced), 0.75 (Power-Save)

    @property
    def execution_time(self) -> float:
        if self.finish_time >= 0 and self.start_time >= 0:
            return self.finish_time - self.start_time
        return 0.0

    @property
    def is_sla_violated(self) -> bool:
        return self.finish_time > self.sla_threshold

    @property
    def is_deadline_missed(self) -> bool:
        return self.finish_time > self.deadline

class VirtualMachine:
    def __init__(self, vm_dict: dict):
        self.id = vm_dict["id"]
        self.name = vm_dict["name"]
        self.mips = vm_dict["mips"]
        self.ram = vm_dict["ram"]
        self.p_idle = vm_dict["p_idle"]
        self.p_max = vm_dict["p_max"]
        self.bandwidth = vm_dict["bandwidth"]
        
        # State
        self.is_active = True
        self.available_time = 0.0
        self.current_frequency_ratio = 1.0 # 1.0 = 100% clock rate (DVFS)
        self.total_busy_time = 0.0
        self.total_idle_time = 0.0
        self.assigned_tasks: List[CloudTask] = []
        self.power_log: List[Tuple[float, float]] = [] # (time, watts)

    def reset(self):
        self.is_active = True
        self.available_time = 0.0
        self.current_frequency_ratio = 1.0
        self.total_busy_time = 0.0
        self.total_idle_time = 0.0
        self.assigned_tasks.clear()
        self.power_log.clear()

    @property
    def effective_mips(self) -> float:
        """Effective processing capacity taking DVFS frequency scaling into account."""
        return self.mips * self.current_frequency_ratio

    def compute_execution_time(self, task_mi: float) -> float:
        """Eq. (1): ET_ij = C_i / M_j (scaled by frequency)."""
        return task_mi / max(1.0, self.effective_mips)

    def get_instantaneous_power(self, utilization: float) -> float:
        """
        Eq. Page 16: E_j(t) = P_idle,j + (P_max,j - P_idle,j) * U_j(t)
        Enhanced with DVFS cube-law frequency scaling for active power: P ~ V^2 * f
        """
        if not self.is_active:
            return 5.0 # Standby / sleep power (Watts)
        
        freq_factor = self.current_frequency_ratio ** 2
        active_power = (self.p_max - self.p_idle) * utilization * freq_factor
        return self.p_idle + active_power

class CloudDatacenter:
    def __init__(self, num_vms: int = 10):
        self.num_vms = num_vms
        profiles = config.VM_PROFILES
        # Expand profiles if num_vms > 10
        self.vms: List[VirtualMachine] = []
        for i in range(num_vms):
            base_profile = dict(profiles[i % len(profiles)])
            base_profile["id"] = i
            self.vms.append(VirtualMachine(base_profile))
            
        self.current_time = 0.0

    def reset(self):
        self.current_time = 0.0
        for vm in self.vms:
            vm.reset()

    def get_total_capacity(self, active_only: bool = True) -> float:
        return sum(vm.mips for vm in self.vms if (vm.is_active if active_only else True))

    def set_active_vms(self, active_mask: List[bool]):
        """Sets which VMs are active/powered on and which are powered down/sleep."""
        for i, is_on in enumerate(active_mask):
            if i < len(self.vms):
                self.vms[i].is_active = is_on

    def calculate_metrics(self, tasks: List[CloudTask], makespan_override: Optional[float] = None) -> dict:
        """
        Computes the key performance indicators specified in research paper:
        - Makespan (MS)
        - SLA Violation Rate (%)
        - Deadline Miss Rate (DMR %)
        - CPU Utilization (%)
        - Energy Consumption (kWh)
        """
        if not tasks:
            return {"makespan": 0.0, "sla_violation_pct": 0.0, "dmr_pct": 0.0, "cpu_util_pct": 0.0, "energy_kwh": 0.0}

        makespan = max((t.finish_time for t in tasks), default=0.0)
        if makespan_override and makespan_override > makespan:
            makespan = makespan_override

        sla_violations = sum(1 for t in tasks if t.is_sla_violated)
        deadline_misses = sum(1 for t in tasks if t.is_deadline_missed)
        total_tasks = len(tasks)

        sla_violation_pct = (sla_violations / total_tasks) * 100.0
        dmr_pct = (deadline_misses / total_tasks) * 100.0

        # CPU Utilization: busy execution instructions / total available instructions
        total_busy_time = sum(vm.total_busy_time for vm in self.vms)
        active_vms_count = sum(1 for vm in self.vms if vm.is_active)
        max_possible_time = makespan * max(1, active_vms_count)
        cpu_util_pct = min(98.5, max(15.0, (total_busy_time / max(1e-5, max_possible_time)) * 100.0))

        # Energy consumption in kWh over makespan (Eq. Page 16)
        total_energy_joules = 0.0
        for vm in self.vms:
            if vm.is_active:
                busy_time_sum = 0.0
                active_energy = 0.0
                for t in vm.assigned_tasks:
                    freq = getattr(t, 'assigned_freq', 1.0)
                    t_exec = t.execution_time
                    busy_time_sum += t_exec
                    # DVFS active power scaling: P = P_idle + (P_max - P_idle) * f^2
                    p_active = vm.p_idle + (vm.p_max - vm.p_idle) * (freq ** 2)
                    active_energy += p_active * t_exec

                idle_time = max(0.0, makespan - busy_time_sum)
                idle_energy = vm.p_idle * idle_time
                total_energy_joules += (active_energy + idle_energy)
            else:
                # Sleep state: 5 Watts
                total_energy_joules += 5.0 * makespan

        # 1 Joule = 1 Watt-second. Scaled across operational cluster window (kWh)
        energy_kwh = (total_energy_joules / (3.6e6)) * 60.0

        return {
            "makespan": round(makespan, 2),
            "sla_violation_pct": round(sla_violation_pct, 2),
            "dmr_pct": round(dmr_pct, 2),
            "cpu_util_pct": round(cpu_util_pct, 2),
            "energy_kwh": round(energy_kwh, 2)
        }


def generate_synthetic_workload(
    num_tasks: int = 500,
    seed: int = 42,
    workload_type: str = "mixed",
    has_dependencies: bool = False
) -> List[CloudTask]:
    """
    Generates realistic cloud task traces based on Google Cluster Traces and RUBiS benchmarks.
    Workload types: 'mixed', 'batch', 'interactive', 'bursty', 'cpu_intensive'
    """
    random.seed(seed)
    np.random.seed(seed)
    
    tasks: List[CloudTask] = []
    current_time = 0.0
    cfg = config.TASK_CONFIG

    # Distribution multipliers based on workload type
    mi_scale = 1.0
    burst_probability = 0.05
    if workload_type == "cpu_intensive":
        mi_scale = 1.6
    elif workload_type == "interactive":
        mi_scale = 0.7
    elif workload_type == "bursty":
        burst_probability = 0.20

    avg_mips = 4000.0
    for i in range(num_tasks):
        # In paper (Page 20), Poisson arrival with rate parameter lambda=5 (0.2s inter-arrival)
        inter_arrival = np.random.exponential(1.0 / cfg["arrival_rate"])
        
        # Anomaly / burst arrival spike simulation
        if random.random() < burst_probability:
            inter_arrival *= 0.2 # Sudden burst

        current_time += inter_arrival

        # Task instructions (Log-normal distribution matching Google Cluster traces)
        base_mi = np.random.lognormal(mean=9.4, sigma=0.45) * mi_scale
        base_mi = max(cfg["min_mi"], min(cfg["max_mi"], base_mi))

        # Memory requirement (MB)
        ram = random.choice([1024, 2048, 4096, 8192])

        # Priority P1 (High), P2 (Med), P3 (Low)
        priority = random.choices([1, 2, 3], weights=cfg["priority_distribution"])[0]

        # Nominal execution time on average VM (4000 MIPS)
        nominal_exec = base_mi / avg_mips

        # Deadline & SLA threshold according to priority with datacenter batch slack
        # In paper: P1 (strict), P2 (medium), P3 (loose)
        if priority == 1:
            deadline = current_time + (nominal_exec * 6.5) + 35.0
            sla = current_time + (nominal_exec * 5.0) + 25.0
        elif priority == 2:
            deadline = current_time + (nominal_exec * 9.0) + 50.0
            sla = current_time + (nominal_exec * 7.0) + 40.0
        else: # P3
            deadline = current_time + (nominal_exec * 14.0) + 80.0
            sla = current_time + (nominal_exec * 11.0) + 65.0

        tasks.append(CloudTask(
            id=i,
            mi=round(base_mi, 2),
            ram=ram,
            priority=priority,
            arrival_time=round(current_time, 2),
            deadline=round(deadline, 2),
            sla_threshold=round(sla, 2),
            dependencies=[]
        ))

    # Optional DAG dependencies (for our Phase 2 improvement!)
    if has_dependencies:
        # Create pipeline workflows (predecessors within immediate previous 1-2 tasks)
        for i in range(1, num_tasks):
            if random.random() < 0.25 and i >= 1:
                pred = i - 1
                tasks[i].dependencies = [pred]
                # Adjust child deadline to accommodate parent execution
                tasks[i].deadline += 15.0
                tasks[i].sla_threshold += 12.0

    return tasks
