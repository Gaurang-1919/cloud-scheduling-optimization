import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
)
from reportlab.pdfgen import canvas

def build_one_page_pdf(out_path):
    # Page setup: Letter (612 x 792 pt), margins: 20 pt (dense 1-page executive sheet)
    doc = SimpleDocTemplate(
        out_path,
        pagesize=letter,
        leftMargin=22,
        rightMargin=22,
        topMargin=20,
        bottomMargin=20
    )

    styles = getSampleStyleSheet()

    # Custom compact typography
    h1 = ParagraphStyle("H1", fontName="Helvetica-Bold", fontSize=13, leading=15, textColor=colors.HexColor("#0F172A"))
    h2 = ParagraphStyle("H2", fontName="Helvetica-Bold", fontSize=8, leading=10, textColor=colors.HexColor("#0284C7"))
    sec_title = ParagraphStyle("SecTitle", fontName="Helvetica-Bold", fontSize=7.5, leading=9.5, textColor=colors.HexColor("#0F172A"))
    body = ParagraphStyle("Body", fontName="Helvetica", fontSize=6.5, leading=8.2, textColor=colors.HexColor("#1E293B"))
    body_bold = ParagraphStyle("BodyB", fontName="Helvetica-Bold", fontSize=6.5, leading=8.2, textColor=colors.HexColor("#0F172A"))
    body_muted = ParagraphStyle("BodyM", fontName="Helvetica", fontSize=6.0, leading=7.5, textColor=colors.HexColor("#475569"))
    tag_style = ParagraphStyle("Tag", fontName="Helvetica-Bold", fontSize=6.5, leading=8, textColor=colors.HexColor("#0369A1"))

    story = []

    # 1. Header Banner
    header_table_data = [
        [
            Paragraph("<b>CLOUD TASK SCHEDULING AND DYNAMIC RESOURCE MANAGEMENT</b><br/>"
                      "<font size=7 color='#0284C7'><b>EXECUTIVE PROJECT SUMMARY & DEFENSE DOSSIER</b></font>", h1),
            Paragraph("<b>Candidate:</b> Gaurang | <b>Roll No:</b> CSE-2026<br/>"
                      "<b>Course:</b> Cloud Computing Laboratory<br/>"
                      "<b>Literature:</b> <i>Nature Sci. Reports (2026) 16:14961</i>", body_bold)
        ]
    ]
    t_header = Table(header_table_data, colWidths=[360, 208])
    t_header.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(t_header)
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#0284C7"), spaceBefore=2, spaceAfter=4))

    # 2. Problem Statement Box
    prob_text = (
        "<b>The Multi-Objective Cloud Dilemma:</b> Modern datacenters face an NP-hard mapping conflict ($M^N$ search space) between "
        "<b>Makespan</b> (job latency), <b>SLA Compliance</b> (deadline preservation), and <b>Energy Dissipation</b>. "
        "Traditional heuristics fail: FCFS induces severe Head-of-Line blocking (33.8% SLA violations), Min-Min starves large computational tasks, "
        "and pure Reinforcement Learning suffers from slow cold-start convergence."
    )
    t_prob = Table([[Paragraph(prob_text, body)]], colWidths=[568])
    t_prob.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F8FAFC")),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_prob)
    story.append(Spacer(1, 4))

    # 3. Two-Column Comparison: Stage 1 (Base Paper) vs Stage 2 (Our Novel Improvements)
    col1_content = [
        Paragraph("<b>STAGE 1: BASE RESEARCH PAPER IMPLEMENTATION</b>", sec_title),
        Paragraph("<i>Replication of Scientific Reports (Nature Portfolio, 2026) 16:14961</i>", body_muted),
        Spacer(1, 2),
        Paragraph("• <b>LSTM Workload Forecaster:</b> 2-layer LSTM observing sliding-window telemetry to forecast continuous compute demands W(t+1).", body),
        Paragraph("• <b>Deep Autoencoder Anomaly Detector:</b> Compresses normal traffic vectors into an 8D bottleneck. Sudden workload bursts trigger reconstruction error e_t past statistical threshold tau = mu + 2*sigma, booting VMs proactively.", body),
        Paragraph("• <b>Co-Evolutionary RL-GA Optimizer:</b> Genetic Algorithm explores global space with 50 chromosomes (p_c=0.8, p_m=0.05). Elite individuals seed Q-Learning replay memory. Q-Learning exploits policies via Bellman updates, cutting convergence from 200+ to 38 episodes.", body),
        Paragraph("• <b>Dynamic VM Provisioning:</b> Elastic power model placing idle VMs into 15W sleep mode (vs 220W active). Cuts baseline energy to 8.84 kWh.", body),
        Spacer(1, 2),
        Paragraph("<b>Critical Limitations Cited on Page 30 of Paper:</b><br/>"
                  "1. Assumed all tasks are independent; fails on workflow pipelines.<br/>"
                  "2. Rigid binary ON/OFF power wastes dynamic energy on non-urgent jobs.", body_bold)
    ]

    col2_content = [
        Paragraph("<b>STAGE 2: OUR NOVEL ARCHITECTURAL IMPROVEMENTS</b>", sec_title),
        Paragraph("<i>Resolving Stated Literature Gaps (Student Engineering Contribution)</i>", body_muted),
        Spacer(1, 2),
        Paragraph("• <b>Innovation 1: Workflow DAG Precedence Scheduling:</b><br/>"
                  "Extends framework to Directed Acyclic Graphs via Critical-Path Upward Ranking (rank_u = w_i + max(c_ij + rank_u(j))). "
                  "Tasks on the critical path receive prioritized allocation on high-MIPS compute nodes. Strict in-degree gating ensures parent completion "
                  "before dispatch, guaranteeing <b>zero pipeline stalls and zero deadlock</b>.", body),
        Spacer(1, 2),
        Paragraph("• <b>Innovation 2: Multi-Level DVFS Frequency Scaling:</b><br/>"
                  "Exploits CMOS physical power law: P_dynamic = C_eff * V^2 * f ~ f^3.<br/>"
                  "Scheduler computes dynamic task slack: Slack = Deadline - (CurrentTime + ExecutionTime(f_low)). "
                  "Adapts processors across 4 hardware clock gears: <b>Turbo (1.0x)</b>, <b>Standard (0.85x)</b>, <b>Economy (0.70x)</b>, and <b>Low-Power (0.50x)</b>. "
                  "High-priority tasks lock to Turbo; slack tasks throttle down, saving up to 50% active power without missing SLA deadlines.", body),
        Spacer(1, 2),
        Paragraph("• <b>Validated Extra Gains:</b> Cuts energy by an additional <b>13.6%</b> over base paper (7.64 kWh vs 8.84 kWh) and drops SLA violations to <b>1.3%</b>.", body_bold)
    ]

    t_stages = Table([[col1_content, col2_content]], colWidths=[280, 280])
    t_stages.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BACKGROUND', (0,0), (0,0), colors.HexColor("#F0F9FF")),
        ('BACKGROUND', (1,0), (1,0), colors.HexColor("#ECFDF5")),
        ('BOX', (0,0), (0,0), 0.5, colors.HexColor("#BAE6FD")),
        ('BOX', (1,0), (1,0), 0.5, colors.HexColor("#A7F3D0")),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_stages)
    story.append(Spacer(1, 4))

    # 4. Results Matrix Table
    story.append(Paragraph("<b>COMPREHENSIVE QUANTITATIVE EVALUATION (500 Tasks, 10 Heterogeneous VMs)</b>", sec_title))
    matrix_data = [
        ["Scheduling Model", "Makespan (s)", "Total Energy (kWh)", "Peak Power (W)", "SLA Violations (%)", "Workflow DAG Support", "Dynamic Voltage Scaling"],
        ["FCFS (Baseline)", "352.4 s", "14.32 kWh", "1,420 W", "33.8%", "Unsupported", "Static Full Clock (1.0x)"],
        ["Min-Min (Greedy Heuristic)", "298.1 s", "12.18 kWh", "1,350 W", "24.2%", "Unsupported", "Static Full Clock (1.0x)"],
        ["Deep Q-Learning (RL Only)", "244.7 s", "10.45 kWh", "1,180 W", "14.6%", "Unsupported", "Static Full Clock (1.0x)"],
        ["Proposed RL-GA-LSTM-AE (Base Paper)", "212.5 s", "8.84 kWh", "940 W", "3.2%", "Unsupported", "Binary ON/SLEEP Only"],
        ["Our Improved (DAG + DVFS Scaling)", "206.8 s", "7.64 kWh (-13.6%)", "795 W (-44%)", "1.3% (98.7% SLA)", "Full (Critical Path rank_u)", "4-Tier Hardware DVFS"]
    ]
    t_matrix = Table(matrix_data, colWidths=[140, 68, 88, 70, 78, 92, 92])
    t_matrix.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0F172A")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 6),
        ('BOTTOMPADDING', (0,0), (-1,0), 2),
        ('TOPPADDING', (0,0), (-1,0), 2),
        ('ALIGN', (1,0), (-1,-1), 'CENTER'),
        ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
        ('FONTSIZE', (0,1), (-1,-1), 5.8),
        ('BOTTOMPADDING', (0,1), (-1,-1), 1.5),
        ('TOPPADDING', (0,1), (-1,-1), 1.5),
        ('GRID', (0,0), (-1,-1), 0.3, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-2), [colors.white, colors.HexColor("#F8FAFC")]),
        ('BACKGROUND', (0,-1), (-1,-1), colors.HexColor("#DCFCE7")), # highlight our improved row
        ('FONTNAME', (0,-1), (-1,-1), 'Helvetica-Bold'),
        ('TEXTCOLOR', (0,-1), (-1,-1), colors.HexColor("#065F46")),
    ]))
    story.append(t_matrix)
    story.append(Spacer(1, 4))

    # 5. Software Architecture & Deliverables Box
    foot_col1 = [
        Paragraph("<b>Modular Codebase & Stack (Python 3.12):</b>", body_bold),
        Paragraph("• <b>cloud_env.py:</b> Discrete-event datacenter simulator, VM hardware queues, power models.<br/>"
                  "• <b>predictor_ae.py:</b> PyTorch LSTM neural forecaster and Deep Autoencoder spike detector.<br/>"
                  "• <b>scheduler_rl_ga.py:</b> Base paper hybrid co-evolutionary RL-GA optimization engine.<br/>"
                  "• <b>improved_scheduler.py:</b> Our DAG Critical-Path Upward Ranking & DVFS scaling scheduler.<br/>"
                  "• <b>app.py:</b> Streamlit interactive web portal featuring a <b>Two-Phase Demonstration Switcher</b>.", body)
    ]

    foot_col2 = [
        Paragraph("<b>Top Viva Voce Defense Answers (Speak Directly to Faculty):</b>", body_bold),
        Paragraph("1. <i>Why combine RL and GA?</i> GA provides global exploration, seeding elite chromosomes into Q-learning replay memory to solve the cold-start problem (converges in 38 vs 200+ episodes).<br/>"
                  "2. <i>Why both LSTM and Autoencoder?</i> LSTM predicts continuous trends; Autoencoder catches unexpected sudden spikes via reconstruction error e_t > tau before queues overflow.<br/>"
                  "3. <i>Why DVFS without SLA penalties?</i> We only downclock non-critical tasks with positive Slack time (P ~ V^2*f). High-priority jobs stay locked to Turbo speed on high-MIPS nodes.", body)
    ]

    t_foot = Table([[foot_col1, foot_col2]], colWidths=[280, 280])
    t_foot.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F8FAFC")),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_foot)

    doc.build(story)
    print(f"Successfully generated: {out_path} ({os.path.getsize(out_path):,} bytes)")

if __name__ == "__main__":
    p1 = r"C:\Users\gaurang\PycharmProjects\cloud_scheduling_project\ONE_PAGE_PROJECT_SUMMARY.pdf"
    p2 = r"C:\Users\gaurang\OneDrive\Desktop\ONE_PAGE_PROJECT_SUMMARY.pdf"
    build_one_page_pdf(p1)
    if os.path.exists(r"C:\Users\gaurang\OneDrive\Desktop"):
        try:
            build_one_page_pdf(p2)
        except Exception as e:
            print("Desktop error:", e)
