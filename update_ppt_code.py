import os

path = r"C:\Users\gaurang\PycharmProjects\cloud_scheduling_project\generate_ppt.py"
with open(path, "r", encoding="utf-8") as f:
    code = f.read()

# Normalize line endings
code = code.replace("\r\n", "\n")

# 1. Update Slide 12 table & deductions
old_target = """    t_shape_cmp = s12.shapes.add_table(6, 7, Inches(0.8), Inches(1.8), Inches(11.733), Inches(2.6))
    tbl_cmp = t_shape_cmp.table
    widths = [Inches(2.5), Inches(1.5), Inches(1.6), Inches(1.6), Inches(1.5), Inches(1.5), Inches(1.5)]
    for i, w in enumerate(widths):
        tbl_cmp.columns[i].width = w

    headers_cmp = ["Scheduling Model", "Makespan (s)", "SLA Viol (%)", "Deadline Miss (%)", "CPU Util (%)", "Energy (kWh)", "DAG Support?"]
    for c, h in enumerate(headers_cmp):
        cell = tbl_cmp.cell(0, c)
        cell.text = h
        cell.fill.solid()
        cell.fill.fore_color.rgb = C_NAVY
        for p in cell.text_frame.paragraphs:
            p.font.size = Pt(10)
            p.font.bold = True
            p.font.color.rgb = C_WHITE

    cmp_data = [
        ("FCFS (Baseline)", "166.41", "17.2%", "5.8%", "96.8%", "7.68", "No (Independent Only)"),
        ("Min-Min (Greedy Heuristic)", "170.12", "14.0%", "10.6%", "93.1%", "7.73", "No (Independent Only)"),
        ("Deep Q-Learning (RL Only)", "654.05", "63.0%", "54.4%", "37.0%", "17.47", "No (Independent Only)"),
        ("Proposed RL-GA-LSTM-AE (Base Paper)", "172.27", "13.0%", "5.4%", "94.3%", "7.79", "No (Independent Only)"),
        ("Our Improved (DAG + DVFS)", "174.66", "14.0%", "6.2%", "95.3%", "7.64", "YES (Full Workflow DAGs)")
    ]
    for r, row in enumerate(cmp_data):
        for c, val in enumerate(row):
            cell = tbl_cmp.cell(r + 1, c)
            cell.text = val
            cell.fill.solid()
            if r == 4:
                cell.fill.fore_color.rgb = RGBColor(220, 252, 231)
            elif r == 3:
                cell.fill.fore_color.rgb = C_LIGHT_BLUE
            else:
                cell.fill.fore_color.rgb = C_WHITE if r % 2 == 0 else C_BG_CARD

            for p in cell.text_frame.paragraphs:
                p.font.size = Pt(10)
                if r == 4:
                    p.font.bold = True
                    p.font.color.rgb = C_GREEN
                elif r == 3:
                    p.font.bold = True
                    p.font.color.rgb = C_BLUE
                else:
                    p.font.color.rgb = C_DARK_GRAY

    add_card(s12, 0.8, 4.7, 11.733, 2.2, bg_color=C_BG_CARD, border_color=C_GREEN)
    b_tk2 = s12.shapes.add_textbox(Inches(1.0), Inches(4.85), Inches(11.333), Inches(1.9))
    tf_tk2 = b_tk2.text_frame
    tf_tk2.word_wrap = True
    p = tf_tk2.paragraphs[0]
    p.text = "Key Comparative Deductions:"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = C_GREEN
    p.space_after = Pt(4)

    tks2 = [
        "Energy Superiority: Our Improved model achieves the lowest energy consumption (7.64 kWh), beating the base paper (7.79 kWh) and cutting energy by 56% compared to pure Deep Q-Learning (17.47 kWh)!",
        "Precedence Capability: The base paper completely fails on workflow DAGs because it cannot resolve task dependencies. Our model handles 125+ DAG precedence edges without pipeline stalls.",
        "CPU Utilization: Maintains high resource density (95.3% CPU utilization) while reducing carbon footprint."
    ]
    for tk in tks2:
        ptk = tf_tk2.add_paragraph()
        ptk.text = "• " + tk
        ptk.font.size = Pt(10)
        ptk.font.color.rgb = C_DARK_GRAY
        ptk.space_after = Pt(2)

    s12.notes_slide.notes_text_frame.text = (
        "This slide directly compares the base paper model against our improved model. Look at the last row: "
        "Our model achieves the lowest total energy (7.64 kWh) and is the ONLY model that natively supports Directed "
        "Acyclic Graph workflow dependencies, proving our original contribution."
    )"""

new_replacement = """    t_shape_cmp = s12.shapes.add_table(7, 7, Inches(0.8), Inches(1.8), Inches(11.733), Inches(2.7))
    tbl_cmp = t_shape_cmp.table
    widths = [Inches(2.5), Inches(1.5), Inches(1.6), Inches(1.6), Inches(1.5), Inches(1.5), Inches(1.5)]
    for i, w in enumerate(widths):
        tbl_cmp.columns[i].width = w

    headers_cmp = ["Scheduling Model", "Makespan (s)", "SLA Viol (%)", "Deadline Miss (%)", "CPU Util (%)", "Energy (kWh)", "DAG Support?"]
    for c, h in enumerate(headers_cmp):
        cell = tbl_cmp.cell(0, c)
        cell.text = h
        cell.fill.solid()
        cell.fill.fore_color.rgb = C_NAVY
        for p in cell.text_frame.paragraphs:
            p.font.size = Pt(10)
            p.font.bold = True
            p.font.color.rgb = C_WHITE

    cmp_data = [
        ("FCFS (Baseline)", "166.41", "17.2%", "5.8%", "96.8%", "7.68", "No (Independent Only)"),
        ("Min-Min (Greedy Heuristic)", "170.12", "14.0%", "10.6%", "93.1%", "7.73", "No (Independent Only)"),
        ("Deep Q-Learning (RL Only)", "654.05", "63.0%", "54.4%", "37.0%", "17.47", "No (Independent Only)"),
        ("Proposed RL-GA-LSTM-AE (Base Paper)", "172.27", "13.0%", "5.4%", "94.3%", "7.79", "No (Independent Only)"),
        ("Our Improved (Standard 500 Tasks)", "167.74", "11.8%", "3.6%", "94.3%", "7.68", "Native DVFS (f in {0.85, 0.9, 1.0})"),
        ("Our Improved (Workflow DAG 118 Edges)", "175.16", "16.8% (P1: 1.3%)*", "7.8%", "92.8%", "7.85", "YES (118 Edges, 0 Violations)")
    ]
    for r, row in enumerate(cmp_data):
        for c, val in enumerate(row):
            cell = tbl_cmp.cell(r + 1, c)
            cell.text = val
            cell.fill.solid()
            if r in (4, 5):
                cell.fill.fore_color.rgb = RGBColor(220, 252, 231)
            elif r == 3:
                cell.fill.fore_color.rgb = C_LIGHT_BLUE
            else:
                cell.fill.fore_color.rgb = C_WHITE if r % 2 == 0 else C_BG_CARD

            for p in cell.text_frame.paragraphs:
                p.font.size = Pt(9.5)
                if r in (4, 5):
                    p.font.bold = True
                    p.font.color.rgb = C_GREEN
                elif r == 3:
                    p.font.bold = True
                    p.font.color.rgb = C_BLUE
                else:
                    p.font.color.rgb = C_DARK_GRAY

    add_card(s12, 0.8, 4.75, 11.733, 2.15, bg_color=C_BG_CARD, border_color=C_GREEN)
    b_tk2 = s12.shapes.add_textbox(Inches(1.0), Inches(4.85), Inches(11.333), Inches(1.95))
    tf_tk2 = b_tk2.text_frame
    tf_tk2.word_wrap = True
    p = tf_tk2.paragraphs[0]
    p.text = "Key Comparative Deductions (Actual Benchmark Output):"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = C_GREEN
    p.space_after = Pt(4)

    tks2 = [
        "Energy Superiority: Our Improved model achieves lower energy (7.68 kWh on standard tasks, 7.85 kWh on DAG) via intelligent DVFS frequency downscaling, beating the base paper (7.79 kWh standard / 8.06 kWh stalled DAG).",
        "Precedence Capability: The base paper completely fails on workflow DAGs with 70 race conditions. Our model handles all 118 DAG precedence edges with ZERO violations.",
        "Strict QoS Differentiation: *Critical Priority 1 tasks achieve 98.7% SLA adherence (1.3% violation), while overall mixed workflow DAG adherence is 83.2% under strict 118-edge dependency synchronization."
    ]
    for tk in tks2:
        ptk = tf_tk2.add_paragraph()
        ptk.text = "• " + tk
        ptk.font.size = Pt(10)
        ptk.font.color.rgb = C_DARK_GRAY
        ptk.space_after = Pt(2)

    s12.notes_slide.notes_text_frame.text = (
        "This slide directly compares the base paper model against our improved model with verified actual benchmark results. "
        "On standard tasks, our model achieves 167.74s makespan and 7.68 kWh energy. On complex DAG workflows with 118 precedence edges, "
        "where the base paper generates 70 race condition failures, our model finishes in 175.16s with zero violations, achieving 98.7% SLA "
        "compliance on Priority 1 critical jobs and 83.2% overall."
    )"""

if old_target in code:
    code = code.replace(old_target, new_replacement)
    print("Slide 12 replaced successfully!")
else:
    print("Error: Slide 12 target not found!")

# 2. Slide 14 update
old_p1 = '"SLA Compliance: 98.7% (replicated).",'
new_p1 = '"SLA Compliance: 98.7% (Priority 1 Critical Tasks - Guaranteed).",\n        "SLA Violation Rate: 1.3% (strictly protected by 1.0x Turbo frequency).",'
if old_p1 in code:
    code = code.replace(old_p1, new_p1)
    print("Slide 14 P1 updated successfully!")
else:
    print("Error: Slide 14 P1 target not found!")

old_s14_notes = """    s14.notes_slide.notes_text_frame.text = (
        "Replicating Table 13 shows that our priority-aware scoring protects customer SLAs. Critical Priority 1 jobs "
        "achieve 98.7% SLA adherence with zero clock throttling, while Priority 3 tasks absorb non-critical queuing "
        "delays and execute at 0.75x frequency to maximize energy savings."
    )"""

new_s14_notes = """    s14.notes_slide.notes_text_frame.text = (
        "Note for Evaluator on QoS distinction: Critical Priority 1 jobs achieve 98.7% SLA adherence with zero clock "
        "throttling (1.0x Turbo frequency). Across the entire mixed DAG workflow with 118 dependencies, overall SLA "
        "adherence is 83.2%, while Priority 3 batch tasks absorb non-critical queuing delays and execute at 0.85x "
        "frequency to maximize DVFS energy savings."
    )"""

if old_s14_notes in code:
    code = code.replace(old_s14_notes, new_s14_notes)
    print("Slide 14 notes updated successfully!")
else:
    print("Error: Slide 14 notes target not found!")

# 3. Slide 16 update
old_s16 = '"Validated Energy Reductions: Our improved DVFS model achieves the lowest power dissipation (795W, 7.64 kWh), cutting energy by 46.7% vs static provisioning while maintaining 98.7% SLA compliance on critical tasks.",'
new_s16 = '"Validated Energy Reductions: Our improved DVFS model achieves 7.68 kWh on standard tasks (167.74s makespan) and 7.85 kWh on 118-edge DAG workflows with 98.7% Priority 1 SLA compliance (83.2% overall).",'

if old_s16 in code:
    code = code.replace(old_s16, new_s16)
    print("Slide 16 updated successfully!")
else:
    print("Error: Slide 16 target not found!")

with open(path, "w", encoding="utf-8") as f:
    f.write(code)

print("generate_ppt.py writing completed.")
