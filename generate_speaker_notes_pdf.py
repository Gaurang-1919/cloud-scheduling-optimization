import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether, HRFlowable
)
from reportlab.graphics.shapes import Drawing, Rect, String
from reportlab.pdfgen import canvas

slides_data = [
    {
        "num": 1,
        "time": "25 sec",
        "title": "Cloud Workload Scheduling Optimization: Base Paper Implementation and Novel Architectural Enhancements",
        "thumb_title": "Cloud Workload Scheduling",
        "thumb_sub": "Candidate: Gaurang (CSE-2026)\nBase Paper + Novel DAG & DVFS",
        "say": "Good morning, respected professors. I am Gaurang, enrollment CSE-2026. My project tackles the fundamental trade-off in modern cloud datacenters: balancing task makespan, strict Service Level Agreement deadlines, and energy consumption. My work is divided into two distinct parts: first, a complete replication of a recent 2026 Nature Scientific Reports paper; and second, two original architectural enhancements that solve the paper's explicitly cited limitations. I built this end-to-end and validated it through an interactive simulation dashboard.",
        "watch": "State your enrollment ID clearly. If asked why cloud scheduling is hard, state in one phrase: \"It is an NP-hard multi-objective mapping problem with M^N search complexity.\""
    },
    {
        "num": 2,
        "time": "45 sec",
        "title": "Project Structure: Two-Part Implementation Roadmap",
        "thumb_title": "Project Structure & Roadmap",
        "thumb_sub": "Stage 1: Base Paper Replication\nStage 2: Novel DAG & DVFS Enhancements",
        "say": "Here is the roadmap of my work. Stage 1 is the faithful replication of the 2026 paper by Narsimhulu and Kumar. It combines an LSTM workload forecaster, a Deep Autoencoder for proactive anomaly detection, a hybrid co-evolutionary RL-GA scheduler, and dynamic VM provisioning. Stage 2 addresses the two core gaps left open on page 30 of that paper: extending scheduling from independent tasks to dependent DAG workflows, and replacing binary on/off server states with 4-tier Dynamic Voltage and Frequency Scaling.",
        "watch": "Do not claim you invented Genetic Algorithms or Reinforcement Learning. Emphasize that the novelty lies in the hybridization and the two Phase 2 extensions (DAG workflows and DVFS)."
    },
    {
        "num": 3,
        "time": "20 sec",
        "title": "Stage 1: Replication of Foundational Literature (Nature Scientific Reports, 2026)",
        "thumb_title": "Stage 1: Literature Replication",
        "thumb_sub": "Scientific Reports (2026) 16:14961\nNarsimhulu & Kumar Architecture",
        "say": "Stage 1 replicates the foundational paper titled \"A hybrid RL-GA-LSTM-AE framework for energy-aware and SLA-driven task scheduling in cloud computing environments,\" published in Nature Portfolio's Scientific Reports in 2026. Let us examine the four architectural layers proposed by the authors.",
        "watch": "Know the authors' names: Bommineni Narsimhulu and T. Sampath Kumar. Published in 2026, volume 16, article 14961."
    },
    {
        "num": 4,
        "time": "1 min",
        "title": "Base Paper Architecture: Multi-Objective Cloud Scheduling Framework",
        "thumb_title": "3-Tier Framework Architecture",
        "thumb_sub": "Predictor Layer -> Optimization Core\n-> Dynamic Provisioning Layer",
        "say": "The paper structures the datacenter into three hierarchical layers. Incoming tasks first hit a Predictive Analytics Layer, which forecasts future compute demands and detects sudden traffic spikes. This feeds into the Optimization Core, where a Genetic Algorithm explores the global schedule space while a Deep Q-Network exploits learned assignment policies. Finally, the Resource Provisioning Layer manages physical hardware, putting unneeded servers into a 15-Watt sleep mode. Our replication implements this full pipeline.",
        "watch": "If asked why dynamic provisioning matters: idle servers consume 60% to 70% of peak power doing zero useful work. Switching idle VMs to sleep mode (15 W vs 220 W) is where the base paper's initial energy savings come from."
    },
    {
        "num": 5,
        "time": "1 min",
        "title": "Experimental Testbed: Workload Dataset & Datacenter Cluster Profiles",
        "thumb_title": "Dataset & Cluster Hardware",
        "thumb_sub": "Google Cluster Traces & RUBiS (lambda=5)\n10 Heterogeneous AWS EC2 VMs",
        "say": "Here is our experimental testbed and workload dataset report. To ensure academic realism, our 500-task workload is calibrated against Google Cluster Workload Traces and RUBiS benchmarks following a non-homogeneous Poisson arrival process with rate parameter lambda=5.0. Task lengths range from 5,000 to 80,000 Millions of Instructions. Our cluster features 10 heterogeneous virtual machines mapped to AWS EC2 instance families (c5, m5, r5, t3, and g4dn) with power ratings calibrated against SPECpower benchmarks.",
        "watch": "If asked why Poisson: 'Poisson arrival is the standard stochastic model in cloud datacenters because user requests arrive independently.' Know the 3 priority tiers: P1 (25% critical), P2 (50% medium), and P3 (25% batch)."
    },
    {
        "num": 6,
        "time": "1 min 15 sec",
        "title": "Predictive Analytics Layer: LSTM Forecaster & Deep Autoencoder",
        "thumb_title": "LSTM & Autoencoder Analytics",
        "thumb_sub": "LSTM: Compute Demand W(t+1)\nAE: Anomaly Spike Detection (e > tau)",
        "say": "Here is the predictive engine. A 2-layer LSTM observes a sliding window of historical telemetry to predict upcoming compute demand W_hat(t+1). Simultaneously, a Deep Autoencoder compresses normal workload vectors into an 8-dimensional latent space and reconstructs them. Normal traffic reconstructs cleanly with low error. When an unexpected flash crowd arrives, the reconstruction error e_t surges past our statistical threshold tau = mu + 2*sigma. This triggers the datacenter to boot up sleep-state VMs proactively, before queues overflow.",
        "watch": "If asked why you need both: \"LSTM is a continuous regression predictor; Autoencoder is an unsupervised anomaly detector. When a sudden burst happens, LSTM lags by several steps, but the Autoencoder's reconstruction error spikes immediately.\" The threshold uses k=2.0, corresponding to a Chebyshev 95% confidence bound."
    },
    {
        "num": 7,
        "time": "1 min 15 sec",
        "title": "Optimization Core: Co-Evolutionary RL-GA Hybridization",
        "thumb_title": "Co-Evolutionary RL-GA Core",
        "thumb_sub": "GA: Global Chromosome Search\nRL: Q-Learning Local Exploitation",
        "say": "Next is the scheduling brain. Pure Reinforcement Learning suffers from the cold-start problem: in a vast search space, random exploration takes hundreds of episodes to find acceptable schedules. The Genetic Algorithm solves this through global exploration: 50 candidate chromosome schedules undergo single-point crossover and mutation. We take the elite schedules from GA and inject them into the Q-learning replay memory. Q-learning then fine-tunes the policy using Bellman updates. This hybrid co-evolution cuts convergence time from over 200 episodes down to just 38 episodes.",
        "watch": "Be ready to define the chromosome: \"A vector of length N, where index i represents task i, and the integer value represents the assigned VM ID.\" Crossover probability is p_c = 0.8, mutation probability is p_m = 0.05."
    },
    {
        "num": 8,
        "time": "1 min",
        "title": "Mathematical Modeling: Execution, Power, and VM Scoring",
        "thumb_title": "Mathematical Formulations",
        "thumb_sub": "T_exec = MI / MIPS\nReward = -(w1*MS + w2*E + w3*SLA)",
        "say": "This slide formalizes the mathematics from page 15 of the paper. Task execution time on a heterogeneous VM is computational demand in Millions of Instructions divided by VM MIPS. Total datacenter power sums active VMs at 220 Watts and idle VMs at 15 Watts. The Q-learning reward function is explicitly multi-objective: negative weighted sum of makespan, total energy, and an SLA violation penalty. By tuning these weights, the operator balances execution speed against electricity costs.",
        "watch": "The default weights in our benchmark are w_makespan = 0.4, w_energy = 0.4, and w_sla = 0.2. The minus sign is crucial because RL maximizes reward, which corresponds to minimizing cost."
    },
    {
        "num": 9,
        "time": "1 min",
        "title": "Base Paper Replication: Results & Baseline Comparisons (Table 3)",
        "thumb_title": "Base Paper Replication Results",
        "thumb_sub": "Table 3: FCFS vs Min-Min vs RL vs Paper\nMakespan: 352s -> 212s | SLA: 33.8% -> 3.2%",
        "say": "Here are our replicated results across 500 tasks on 10 heterogeneous VMs, matching Table 3 of the paper. Traditional FCFS has severe head-of-line blocking: makespan is 352 seconds, with 33.8% SLA violations and 14.3 kWh energy. Min-Min reduces makespan to 298 seconds by prioritizing small tasks, but starves large ones. The base paper's hybrid RL-GA brings makespan down to 212.5 seconds, cuts energy to 8.84 kWh, and reduces SLA violations to 3.2%. We have successfully validated the paper's claims.",
        "watch": "\"DMR\" in the table stands for Deadline Miss Ratio. Notice that while Min-Min seems fast, its energy is high because it leaves slower VMs idle while hammering the fastest VMs."
    },
    {
        "num": 10,
        "time": "20 sec",
        "title": "Stage 2: Novel Architectural Enhancements (Addressing Cited Limitations)",
        "thumb_title": "Stage 2: Novel Enhancements",
        "thumb_sub": "Addressing Page 30 Paper Limits\n1. Workflow DAGs | 2. Multi-Level DVFS",
        "say": "Now I move to Stage 2: my original research contributions. On page 30, Section 6 of the base paper, the authors explicitly listed their limitations: their model cannot schedule workflow graphs with dependencies, and its energy model is strictly binary. I designed and implemented solutions to both problems.",
        "watch": "Pause after this slide. This transition is your defense stronghold: it shows the panel you read the paper critically and did not simply copy code."
    },
    {
        "num": 11,
        "time": "1 min 15 sec",
        "title": "Improvement 1: Workflow DAG Precedence via Critical-Path Upward Ranking",
        "thumb_title": "DAG Precedence Scheduling",
        "thumb_sub": "Critical-Path Upward Rank (rank_u)\nZero Deadlocks | Zero Pipeline Stalls",
        "say": "My first improvement extends scheduling to Directed Acyclic Graphs. Real cloud workloads—like Spark pipelines and machine learning workflows—have parent-child dependencies. Child tasks cannot execute until parents complete and transfer output data. I implemented Critical-Path Upward Ranking (rank_u). We traverse the DAG backwards from exit nodes, calculating each task's computational cost plus the maximum communication delay to its successors. Tasks on the critical path receive the highest upward rank and get prioritized on fast VMs. Tasks enter the ready queue only when all predecessors finish, guaranteeing zero pipeline stalls and zero deadlock.",
        "watch": "If asked how deadlocks are prevented: \"The graph is mathematically constrained to be a Directed Acyclic Graph (DAG)—no cycles can exist. And tasks are strictly gated by in-degree dependencies: in-degree must reach zero before dispatch.\""
    },
    {
        "num": 12,
        "time": "1 min 15 sec",
        "title": "Improvement 2: Dynamic Voltage & Frequency Scaling (DVFS)",
        "thumb_title": "Multi-Level DVFS Scaling",
        "thumb_sub": "P ~ V^2 * f (Dynamic Power ~ f^3)\nTurbo (1.0x) -> Low Power (0.50x)",
        "say": "My second improvement addresses energy. In CMOS microprocessors, dynamic power follows P proportional to C * V^2 * f. Because supply voltage scales with frequency, dynamic power is proportional to frequency cubed. Running a CPU at 100% turbo frequency for a non-urgent task wastes enormous power. I introduced 4 discrete DVFS operational gears: Turbo at 1.0x clock, Standard at 0.85x, Economy at 0.70x, and Low-Power at 0.50x. For every task, my scheduler computes slack time against its deadline. If positive slack exists, we drop the processor clock to Economy or Low-Power mode. If slack is near zero or the task is Priority 1, we lock it in Turbo mode.",
        "watch": "If asked: \"Doesn't lowering clock frequency increase execution time?\" Answer: \"Yes, T = Instructions / MIPS(f). But we only downclock when Slack > 0. The task finishes later, but strictly before its deadline, saving up to 50% dynamic power on that core.\""
    },
    {
        "num": 13,
        "time": "1 min",
        "title": "Head-to-Head Comparison: Base Paper vs Our Improved Implementation",
        "thumb_title": "Head-to-Head Comparison",
        "thumb_sub": "Energy: 8.84 kWh -> 7.64 kWh (-13.6%)\nSLA: 3.2% -> 1.3% | DAGs Supported",
        "say": "This slide presents our comparative evaluation across 500 tasks. Look at the progression across rows. FCFS uses 14.32 kWh. The base paper drops this to 8.84 kWh through dynamic sleep provisioning. Our improved DVFS model drops this further to 7.64 kWh—an additional 13.6% energy savings over the paper, and a 46.7% reduction versus FCFS. Makespan drops slightly to 206.8 seconds, while SLA violations drop to an industry-grade 1.3%. Most importantly, our model supports full DAG workflows, which the base paper cannot run at all.",
        "watch": "Memorize these three key numbers: 7.64 kWh energy (13.6% lower than paper), 1.3% SLA violations (vs 3.2% paper, 33.8% FCFS), and 206.8s makespan."
    },
    {
        "num": 14,
        "time": "1 min",
        "title": "Power Dynamics: Static vs Base Paper vs Our Improved DVFS (Figure 8)",
        "thumb_title": "Figure 8: Power Profile (W)",
        "thumb_sub": "Static: 1420 W -> Paper: 940 W\nImproved DVFS: 795 W Peak (-44%)",
        "say": "This replicates and extends Figure 8 from the research paper. The red line is static provisioning: servers run at fixed power regardless of workload, consuming roughly 1,420 Watts continuously. The blue line is the base paper: during the low-demand valley between 400 and 600 seconds, idle VMs sleep, dropping power to 940 Watts. The green line is our improved model: by combining sleep states with DVFS frequency throttling during execution, active server power drops even further, stabilizing at 795 Watts peak.",
        "watch": "The dip between 400s and 600s is an artificial low-load interval injected into the synthetic test trace to test sleep transitions. The base paper did this exact test in their Figure 8."
    },
    {
        "num": 15,
        "time": "50 sec",
        "title": "Quality of Service (QoS): Priority-Wise SLA Adherence (Table 13)",
        "thumb_title": "Table 13: QoS & SLA Adherence",
        "thumb_sub": "Priority 1: 98.7% SLA Met (Turbo)\nPriority 3: 89.1% SLA (Absorbs Slack)",
        "say": "Here we replicate Table 13 to verify Quality of Service across task priority classes. In cloud computing, mission-critical tasks must never fail. Our scheduler gives Priority 1 tasks a 98.7% SLA adherence rate and an average response time of 45 seconds, locking them to Turbo DVFS gears. Priority 2 tasks achieve 94.2% compliance. Priority 3 background tasks absorb the queuing delay and clock throttling, achieving 89.1% compliance. This proves our multi-objective reward successfully isolates critical tasks from performance degradation.",
        "watch": "If asked why Priority 3 SLA is 89%: \"Priority 3 tasks are explicitly modeled as low-priority batch jobs (e.g., log indexing). Throttling them to save datacenter power is an intentional, SLA-compliant trade-off.\""
    },
    {
        "num": 16,
        "time": "1 min",
        "title": "Implementation Proof: Modular Codebase & Interactive Portal (app.py)",
        "thumb_title": "Implementation Proof & Codebase",
        "thumb_sub": "cloud_env.py | predictor_ae.py\nscheduler_rl_ga.py | improved_scheduler.py",
        "say": "Everything presented today is backed by an authentic, modular Python codebase and a live interactive portal built with Streamlit. cloud_env.py models the discrete-event datacenter. predictor_ae.py contains the PyTorch LSTM and Autoencoder models. scheduler_rl_ga.py implements the base paper's hybrid algorithm, and improved_scheduler.py contains my DAG and DVFS implementations. The portal features a Two-Phase Live Demonstration Switcher allowing evaluators to test both Phase 1 (Base Paper) and Phase 2 (Our Novel Improvements) with one click.",
        "watch": "Offer to run the code: \"Sir, I have the portal running locally on port 8501 and PyCharm open. I can execute any workload configuration live right now.\""
    },
    {
        "num": 17,
        "time": "45 sec",
        "title": "Conclusions & Technical Summary",
        "thumb_title": "Conclusions & Viva Summary",
        "thumb_sub": "Replication + Original Innovation\n46.7% Energy Cut | 98.7% P1 SLA",
        "say": "To conclude: this project achieves both academic replication and novel research progress. In Stage 1, we fully replicated the 2026 Nature Scientific Reports architecture, validating its forecasting, hybrid optimization, and dynamic sleep provisioning across Google Cluster Traces. In Stage 2, we resolved its cited limitations by introducing DAG Critical-Path Upward Ranking and 4-tier DVFS frequency scaling. The result is a robust cloud scheduling system that cuts energy by 46.7% versus standard baselines and 13.6% versus the base paper, with 98.7% SLA protection on critical workloads. Thank you. I am now ready for viva voce questions.",
        "watch": "End cleanly and confidently. Stop talking and wait for the examiners to ask their questions. Refer back to the exact slide numbers when answering."
    }
]

def create_slide_thumbnail(slide_num, title, sub_text):
    w, h = 135, 82
    d = Drawing(w, h)
    # Background card
    d.add(Rect(0, 0, w, h, fillColor=colors.HexColor("#0F172A"), strokeColor=colors.HexColor("#334155"), strokeWidth=1, rx=4, ry=4))
    # Top accent bar
    d.add(Rect(0, h-4, w, 4, fillColor=colors.HexColor("#0284C7"), strokeColor=None))
    # Slide tag
    d.add(String(8, h-16, f"Slide {slide_num}", fontName="Helvetica-Bold", fontSize=8, fillColor=colors.HexColor("#38BDF8")))
    # Title
    t1 = title[:24]
    t2 = title[24:48] if len(title) > 24 else ""
    d.add(String(8, h-28, t1, fontName="Helvetica-Bold", fontSize=7, fillColor=colors.white))
    if t2:
        d.add(String(8, h-37, t2, fontName="Helvetica-Bold", fontSize=7, fillColor=colors.white))
    
    # Sub box
    d.add(Rect(6, 6, w-12, 30, fillColor=colors.HexColor("#1E293B"), strokeColor=colors.HexColor("#475569"), strokeWidth=0.5, rx=2, ry=2))
    lines = sub_text.split("\n")
    y = 24
    for l in lines[:2]:
        d.add(String(10, y, l[:26], fontName="Helvetica", fontSize=5.5, fillColor=colors.HexColor("#CBD5E1")))
        y -= 10
    return d

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        # Header text
        self.drawString(36, 762, "Speaker notes · Gaurang (CSE-2026) · Cloud Task Scheduling & Resource Management")
        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.setLineWidth(0.5)
        self.line(36, 756, 576, 756)
        
        # Footer text
        self.line(36, 36, 576, 36)
        self.drawString(36, 26, "Distributed Cloud Computing Project Presentation Notes")
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(576, 26, page_str)
        self.restoreState()

def build_pdf(out_path):
    doc = SimpleDocTemplate(
        out_path,
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=46,
        bottomMargin=46
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "DocTitle",
        fontName="Helvetica-Bold",
        fontSize=20,
        leading=24,
        textColor=colors.HexColor("#0F172A"),
        spaceAfter=4
    )

    meta_style = ParagraphStyle(
        "DocMeta",
        fontName="Helvetica",
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#475569"),
        spaceAfter=10
    )

    slide_num_style = ParagraphStyle(
        "SlideNum",
        fontName="Helvetica-Bold",
        fontSize=9.5,
        leading=12,
        textColor=colors.HexColor("#0284C7")
    )

    slide_title_style = ParagraphStyle(
        "SlideTitle",
        fontName="Helvetica-Bold",
        fontSize=11,
        leading=14,
        textColor=colors.HexColor("#0F172A"),
        spaceAfter=5
    )

    say_label_style = ParagraphStyle(
        "SayLabel",
        fontName="Helvetica-Bold",
        fontSize=9,
        leading=12,
        textColor=colors.HexColor("#1E293B"),
        spaceAfter=2
    )

    say_body_style = ParagraphStyle(
        "SayBody",
        fontName="Helvetica",
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor("#1E293B"),
        spaceAfter=5
    )

    watch_label_style = ParagraphStyle(
        "WatchLabel",
        fontName="Helvetica-Bold",
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor("#64748B"),
        spaceAfter=2
    )

    watch_body_style = ParagraphStyle(
        "WatchBody",
        fontName="Helvetica-Oblique",
        fontSize=8,
        leading=10.5,
        textColor=colors.HexColor("#475569")
    )

    story = []

    # Title Banner
    story.append(Paragraph("Speaker notes", title_style))
    story.append(Paragraph(
        "17 slides, about 15 minutes. Results are empirical and simulated across 500 tasks and 10 heterogeneous VMs. Say the \"Say\" text in your own words.",
        meta_style
    ))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#0F172A"), spaceBefore=0, spaceAfter=12))

    for s in slides_data:
        thumb = create_slide_thumbnail(s["num"], s["thumb_title"], s["thumb_sub"])
        
        # Right column content
        r_flowables = [
            Paragraph(f"Slide {s['num']} · {s['time']}", slide_num_style),
            Paragraph(s["title"], slide_title_style),
            Paragraph("Say", say_label_style),
            Paragraph(s["say"], say_body_style),
            Paragraph("If asked / watch out", watch_label_style),
            Paragraph(s["watch"], watch_body_style)
        ]

        table_data = [[thumb, r_flowables]]
        t = Table(table_data, colWidths=[145, 395])
        t.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('LEFTPADDING', (0,0), (-1,-1), 0),
            ('RIGHTPADDING', (0,0), (-1,-1), 0),
            ('TOPPADDING', (0,0), (-1,-1), 2),
            ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ]))

        divider = HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#CBD5E1"), spaceBefore=6, spaceAfter=8)
        story.append(KeepTogether([t, divider]))

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated PDF: {out_path} ({os.path.getsize(out_path):,} bytes)")

if __name__ == "__main__":
    p1 = r"C:\Users\gaurang\PycharmProjects\cloud_scheduling_project\Speaker_Notes_Cloud_Scheduling.pdf"
    p2 = r"C:\Users\gaurang\OneDrive\Desktop\Speaker_Notes_Cloud_Scheduling.pdf"
    build_pdf(p1)
    if os.path.exists(r"C:\Users\gaurang\OneDrive\Desktop"):
        try:
            build_pdf(p2)
        except Exception as e:
            print("Desktop error:", e)
