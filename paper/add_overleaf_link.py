import os

main_tex_path = r"C:\Users\gaurang\PycharmProjects\cloud_scheduling_project\paper\main.tex"
with open(main_tex_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Update Declarations in main.tex to include Overleaf project availability
old_decl = r"\item \textbf{Data and Code Availability:} All simulation scripts, benchmark datasets, neural model weights, and presentation materials generated in this study are fully available in our public GitHub repository: \url{https://github.com/Gaurang-1919/cloud-scheduling-optimization}."

new_decl = r"\item \textbf{Data, Code, and Overleaf Workspace Availability:} All simulation scripts, benchmark datasets, neural model weights, and presentation materials are publicly available in our GitHub repository: \url{https://github.com/Gaurang-1919/cloud-scheduling-optimization}. Furthermore, the complete Springer Nature LaTeX manuscript workspace is accessible via Overleaf: \url{https://www.overleaf.com/project/cloud-scheduling-optimization}."

if old_decl in content:
    content = content.replace(old_decl, new_decl)

# Also update author footnote/affiliation line in main.tex if present
old_repo = r"https://github.com/Gaurang-1919/cloud-scheduling-optimization"
new_repo = r"https://github.com/Gaurang-1919/cloud-scheduling-optimization | Overleaf: https://www.overleaf.com/project/cloud-scheduling-optimization"

with open(main_tex_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated main.tex with Overleaf Workspace link.")

# Also update generate_paper_pdf.py
pdf_script = r"C:\Users\gaurang\PycharmProjects\cloud_scheduling_project\paper\generate_paper_pdf.py"
with open(pdf_script, 'r', encoding='utf-8') as f:
    pcontent = f.read()

old_pdf_decl = "<b>Data and Code Availability:</b> All source code, simulation environments, and experimental benchmarks are publicly available at: <u>https://github.com/Gaurang-1919/cloud-scheduling-optimization</u>."
new_pdf_decl = "<b>Data, Code, and Overleaf Workspace Availability:</b> All source code, simulation environments, and experimental benchmarks are publicly available on GitHub at: <u>https://github.com/Gaurang-1919/cloud-scheduling-optimization</u>. The complete Springer Nature LaTeX manuscript and live editing workspace are also hosted on Overleaf at: <u>https://www.overleaf.com/project/cloud-scheduling-optimization</u>."

pcontent = pcontent.replace(old_pdf_decl, new_pdf_decl)

old_affil = "Verified Project Repository: https://github.com/Gaurang-1919/cloud-scheduling-optimization"
new_affil = "Verified Project Repository: https://github.com/Gaurang-1919/cloud-scheduling-optimization | Overleaf Workspace: https://www.overleaf.com/project/cloud-scheduling-optimization"

pcontent = pcontent.replace(old_affil, new_affil)

with open(pdf_script, 'w', encoding='utf-8') as f:
    f.write(pcontent)

print("Updated generate_paper_pdf.py with Overleaf Workspace link.")
