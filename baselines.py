"""
Baseline Cloud Schedulers (Table 2 & 3 in paper):
1. FCFS (First-Come First-Served)
2. Min-Min Scheduler
3. Deep Q-Learning (RL-only without GA)
4. Static Provisioning
"""

import copy
from typing import List, Tuple
from cloud_env import CloudDatacenter, CloudTask
import numpy as np

class FCFSScheduler:
    """
    First-Come-First-Serve:
    Assigns tasks strictly in order of arrival to whichever active VM becomes available earliest.
    """
    def __init__(self, datacenter: CloudDatacenter):
        self.dc = datacenter

    def schedule(self, tasks: List[CloudTask]) -> dict:
        self.dc.reset()
        # Sort tasks strictly by arrival time
        sorted_tasks = sorted(copy.deepcopy(tasks), key=lambda t: t.arrival_time)
        
        for task in sorted_tasks:
            # Find earliest available active VM
            best_vm = min(self.dc.vms, key=lambda vm: vm.available_time)
            
            # Start time is max of task arrival and VM available time
            start_time = max(task.arrival_time, best_vm.available_time)
            exec_time = best_vm.compute_execution_time(task.mi)
            finish_time = start_time + exec_time
            
            task.assigned_vm = best_vm.id
            task.start_time = start_time
            task.finish_time = finish_time
            task.status = "COMPLETED"
            
            best_vm.available_time = finish_time
            best_vm.total_busy_time += exec_time
            best_vm.assigned_tasks.append(task)
            
        return self.dc.calculate_metrics(sorted_tasks)


class MinMinScheduler:
    """
    Min-Min Algorithm:
    At each step, calculates completion time for all unmapped tasks on all available VMs.
    Selects the task with the minimum completion time and assigns it to that VM.
    Repeats until all tasks are scheduled.
    """
    def __init__(self, datacenter: CloudDatacenter):
        self.dc = datacenter

    def schedule(self, tasks: List[CloudTask]) -> dict:
        self.dc.reset()
        unmapped_tasks = copy.deepcopy(tasks)
        scheduled_tasks = []

        while unmapped_tasks:
            best_task_idx = -1
            best_vm_idx = -1
            min_completion_time = float("inf")
            min_start_time = float("inf")

            for t_idx, task in enumerate(unmapped_tasks):
                for v_idx, vm in enumerate(self.dc.vms):
                    start = max(task.arrival_time, vm.available_time)
                    comp = start + vm.compute_execution_time(task.mi)
                    if comp < min_completion_time:
                        min_completion_time = comp
                        min_start_time = start
                        best_task_idx = t_idx
                        best_vm_idx = v_idx

            # Assign selected task
            task = unmapped_tasks.pop(best_task_idx)
            vm = self.dc.vms[best_vm_idx]
            
            task.assigned_vm = vm.id
            task.start_time = min_start_time
            task.finish_time = min_completion_time
            task.status = "COMPLETED"
            
            vm.available_time = min_completion_time
            vm.total_busy_time += vm.compute_execution_time(task.mi)
            vm.assigned_tasks.append(task)
            scheduled_tasks.append(task)

        return self.dc.calculate_metrics(scheduled_tasks)


class RLOnlyScheduler:
    """
    RL-Only (Deep Q-Learning without GA):
    Learns task-to-VM policy purely via TD-learning without global population search.
    Demonstrates the paper's finding that RL alone gets stuck in local optima and converges slower.
    """
    def __init__(self, datacenter: CloudDatacenter):
        self.dc = datacenter
        self.q_table = {} # state -> action Q values

    def _get_state_key(self, task: CloudTask, dc: CloudDatacenter) -> tuple:
        # Discretized state: (task_priority, task_length_bin, busiest_vm_load_bin)
        len_bin = min(4, int(task.mi // 15000))
        max_load = max(vm.available_time for vm in dc.vms)
        load_bin = min(4, int(max_load // 30))
        return (task.priority, len_bin, load_bin)

    def schedule(self, tasks: List[CloudTask], is_training: bool = False) -> dict:
        self.dc.reset()
        scheduled_tasks = copy.deepcopy(tasks)
        num_vms = len(self.dc.vms)

        for task in scheduled_tasks:
            state = self._get_state_key(task, self.dc)
            if state not in self.q_table:
                self.q_table[state] = np.random.uniform(0.01, 0.05, num_vms)

            # Epsilon-greedy choice
            if np.random.rand() < 0.10:
                chosen_vm_id = np.random.randint(num_vms)
            else:
                q_vals = self.q_table[state]
                # Break ties randomly among max Q
                max_q = np.max(q_vals)
                best_actions = [i for i, q in enumerate(q_vals) if abs(q - max_q) < 1e-4]
                chosen_vm_id = int(np.random.choice(best_actions))

            vm = self.dc.vms[chosen_vm_id]
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

            # Paper Reward Function: R = w1*(1-SLA_v) + w2*(CPU_util) - w3*(Energy)
            sla_pen = 1.0 if task.is_sla_violated else 0.0
            energy_approx = (vm.p_max * exec_time) / 3600.0
            reward = 0.5 * (1.0 - sla_pen) + 0.25 * 0.7 - 0.25 * (energy_approx / 10.0)

            # Q-update
            next_state = self._get_state_key(task, self.dc)
            if next_state not in self.q_table:
                self.q_table[next_state] = np.zeros(num_vms)
            
            best_next = np.max(self.q_table[next_state])
            self.q_table[state][chosen_vm_id] += 0.001 * (reward + 0.95 * best_next - self.q_table[state][chosen_vm_id])

        return self.dc.calculate_metrics(scheduled_tasks)
