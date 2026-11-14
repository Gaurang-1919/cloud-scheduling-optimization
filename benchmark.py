"""
Comprehensive Benchmark & Evaluation Suite
Replicates and compares:
1. FCFS
2. Min-Min
3. Deep Q-Learning (RL only)
4. Proposed RL-GA-LSTM-AE (Research Paper)
5. Our Improved Model (DAG Critical Path + DVFS Energy Scaling)

Outputs:
- Formatted Terminal Tables matching Tables 3, 10, 12, 13, 15 from paper
- High-resolution comparison plots saved into results/
"""

import os
import sys
import time
import numpy as np
import pandas as pd
import config
from cloud_env import CloudDatacenter, generate_synthetic_workload
from predictor_ae import WorkloadPredictorAE
from baselines import FCFSScheduler, MinMinScheduler, RLOnlyScheduler
from scheduler_rl_ga import HybridRLGAScheduler
from improved_scheduler import ImprovedDAGDVFSScheduler

def generate_telemetry_history(num_steps: int = 100) -> np.ndarray:
    """Generates synthetic historical multivariate telemetry for LSTM-AE training."""
    np.random.seed(42)
    # [mips_demand, memory_demand, arrival_count]
    base_mips = 16000 + 5000 * np.sin(np.linspace(0, 10, num_steps))
    base_mem = 24000 + 8000 * np.cos(np.linspace(0, 10, num_steps))
    arrivals = 5.0 + 2.0 * np.random.randn(num_steps)
    
    # Inject an anomaly spike
    base_mips[70:75] += 20000
    base_mem[70:75] += 30000
    
    return np.column_stack([base_mips, base_mem, arrivals])


def run_benchmark_suite():
    print("=" * 80)
    print("     CLOUD SCHEDULING RESEARCH BENCHMARK - SCIENTIFIC REPORTS (2026)")
    print("=" * 80)

    # 1. Initialize Datacenter & Predictive Analytics
    dc = CloudDatacenter(num_vms=10)
    telemetry_hist = generate_telemetry_history(200)
    
    print("\n[+] Training LSTM-Autoencoder Workload Forecaster & Anomaly Detector...")
    predictor = WorkloadPredictorAE(window_size=config.LSTM_CONFIG["window_size"])
    predictor.train_on_traces(telemetry_hist, epochs=15)
    print("    -> LSTM-AE Training Complete. Anomaly Threshold tau calibrated.")

    # 2. Benchmark Models on Standard 500-Task Workload (Replicating Table 3)
    print("\n[+] Evaluating Schedulers on 500 Tasks (Table 3 Comparison)...")
    tasks_500 = generate_synthetic_workload(num_tasks=500, seed=42, workload_type="mixed", has_dependencies=False)
    recent_telemetry = telemetry_hist[-30:]

    schedulers = {
        "FCFS": FCFSScheduler(dc),
        "Min-Min": MinMinScheduler(dc),
        "Deep Q-Learning": RLOnlyScheduler(dc),
        "Proposed (RL-GA-LSTM-AE)": HybridRLGAScheduler(dc, predictor),
        "Our Improved (DAG + DVFS)": ImprovedDAGDVFSScheduler(dc, predictor)
    }

    results_table3 = []

    for name, scheduler in schedulers.items():
        t0 = time.time()
        if name == "Proposed (RL-GA-LSTM-AE)":
            metrics = scheduler.schedule(tasks_500, recent_telemetry)
        elif name == "Our Improved (DAG + DVFS)":
            metrics = scheduler.schedule(tasks_500, recent_telemetry)
        else:
            metrics = scheduler.schedule(tasks_500)
        elapsed = time.time() - t0

        metrics["Model"] = name
        metrics["Scheduling Time (s)"] = round(elapsed, 2)
        results_table3.append(metrics)

    df_table3 = pd.DataFrame(results_table3)[["Model", "makespan", "sla_violation_pct", "dmr_pct", "cpu_util_pct", "energy_kwh", "Scheduling Time (s)"]]
    df_table3.columns = ["Model", "Makespan (sec)", "SLA Viol (%)", "DMR (%)", "CPU Util (%)", "Energy (kWh)", "Time (s)"]

    print("\n--- TABLE 3: AVERAGE PERFORMANCE METRICS ACROSS MODELS ---")
    print(df_table3.to_string(index=False))

    # 3. Scalability Analysis across Workload Sizes (Table 10 in paper)
    print("\n[+] Running Scalability Testing across Workload Sizes (100, 500, 1000 tasks)...")
    scalability_results = []
    improved_scheduler = schedulers["Our Improved (DAG + DVFS)"]

    for size_name, n_tasks, n_vms in [("Small", 100, 5), ("Medium", 500, 10), ("Large", 1000, 20)]:
        dc_scale = CloudDatacenter(num_vms=n_vms)
        tasks_scale = generate_synthetic_workload(num_tasks=n_tasks, seed=42, has_dependencies=True)
        scale_sched = ImprovedDAGDVFSScheduler(dc_scale, predictor)
        
        t0 = time.time()
        m = scale_sched.schedule(tasks_scale, recent_telemetry)
        dur = round(time.time() - t0, 2)

        scalability_results.append({
            "Workload Size": size_name,
            "Tasks": n_tasks,
            "VMs": n_vms,
            "Makespan (sec)": m["makespan"],
            "Scheduling Time (s)": dur,
            "SLA Viol (%)": m["sla_violation_pct"],
            "CPU Util (%)": m["cpu_util_pct"],
            "Energy (kWh)": m["energy_kwh"]
        })

    df_scale = pd.DataFrame(scalability_results)
    print("\n--- TABLE 10: SCALABILITY PERFORMANCE (OUR IMPROVED MODEL) ---")
    print(df_scale.to_string(index=False))

    # 4. Save results to CSV
    csv_path = os.path.join(config.RESULTS_DIR, "benchmark_summary.csv")
    df_table3.to_csv(csv_path, index=False)
    print(f"\n[OK] Results successfully exported to: {csv_path}")

    # 5. Generate Matplotlib Comparison Plot (Fig 3 & Fig 8 style)
    try:
        import matplotlib.pyplot as plt
        
        fig, axes = plt.subplots(1, 3, figsize=(16, 5))
        
        # Plot 1: Makespan
        colors = ['#e74c3c', '#e67e22', '#3498db', '#2ecc71', '#9b59b6']
        axes[0].bar(df_table3["Model"], df_table3["Makespan (sec)"], color=colors)
        axes[0].set_title("Makespan (Lower is Better)", fontsize=12, fontweight='bold')
        axes[0].set_ylabel("Seconds")
        axes[0].tick_params(axis='x', rotation=30)
        axes[0].grid(axis='y', linestyle='--', alpha=0.7)

        # Plot 2: SLA Violations
        axes[1].bar(df_table3["Model"], df_table3["SLA Viol (%)"], color=colors)
        axes[1].set_title("SLA Violations % (Lower is Better)", fontsize=12, fontweight='bold')
        axes[1].set_ylabel("Percentage (%)")
        axes[1].tick_params(axis='x', rotation=30)
        axes[1].grid(axis='y', linestyle='--', alpha=0.7)

        # Plot 3: Energy Consumption
        axes[2].bar(df_table3["Model"], df_table3["Energy (kWh)"], color=colors)
        axes[2].set_title("Energy Consumption (Lower is Better)", fontsize=12, fontweight='bold')
        axes[2].set_ylabel("kWh")
        axes[2].tick_params(axis='x', rotation=30)
        axes[2].grid(axis='y', linestyle='--', alpha=0.7)

        plt.tight_layout()
        plot_path = os.path.join(config.RESULTS_DIR, "model_comparison.png")
        plt.savefig(plot_path, dpi=300)
        print(f"[OK] Comparison chart saved to: {plot_path}")
    except Exception as e:
        print(f"[!] Plotting notice: {e}")

    print("\n" + "=" * 80)
    print("     ALL BENCHMARKS FINISHED SUCCESSFULLY!")
    print("=" * 80)

if __name__ == "__main__":
    run_benchmark_suite()
