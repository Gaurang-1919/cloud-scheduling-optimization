import os

overleaf_url = "https://www.overleaf.com/project/6af89462a6b4fbf99f1afded/share#d1d42196d4c6c82f2e81aac36419c0ccbbd0d131f858b99e"

# 1. Update main.tex
main_tex_path = r"C:\Users\gaurang\PycharmProjects\cloud_scheduling_project\paper\main.tex"
with open(main_tex_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace any previous overleaf template url with the user's exact Overleaf project url
content = content.replace("https://www.overleaf.com/latex/templates/springer-nature-latex-template/gsvvftmrppwq", overleaf_url)

with open(main_tex_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated main.tex with exact user Overleaf share link.")

# 2. Update generate_paper_pdf.py
pdf_script = r"C:\Users\gaurang\PycharmProjects\cloud_scheduling_project\paper\generate_paper_pdf.py"
with open(pdf_script, 'r', encoding='utf-8') as f:
    pcontent = f.read()

pcontent = pcontent.replace("https://www.overleaf.com/latex/templates/springer-nature-latex-template/gsvvftmrppwq", overleaf_url)
pcontent = pcontent.replace("https://www.overleaf.com/project/cloud-scheduling-optimization", overleaf_url)

with open(pdf_script, 'w', encoding='utf-8') as f:
    f.write(pcontent)

print("Updated generate_paper_pdf.py with exact user Overleaf share link.")
