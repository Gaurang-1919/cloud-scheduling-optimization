import os

# Update main.tex with exact live GitHub link (with trailing dash)
main_tex_path = r"C:\Users\gaurang\PycharmProjects\cloud_scheduling_project\paper\main.tex"
with open(main_tex_path, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("https://github.com/Gaurang-1919/cloud-scheduling-optimization",
                          "https://github.com/Gaurang-1919/cloud-scheduling-optimization-")

with open(main_tex_path, 'w', encoding='utf-8') as f:
    f.write(content)

# Update generate_paper_pdf.py
pdf_script = r"C:\Users\gaurang\PycharmProjects\cloud_scheduling_project\paper\generate_paper_pdf.py"
with open(pdf_script, 'r', encoding='utf-8') as f:
    pcontent = f.read()

pcontent = pcontent.replace("https://github.com/Gaurang-1919/cloud-scheduling-optimization",
                            "https://github.com/Gaurang-1919/cloud-scheduling-optimization-")

with open(pdf_script, 'w', encoding='utf-8') as f:
    f.write(pcontent)

print("Synchronized exact GitHub repository link in main.tex and generate_paper_pdf.py.")
