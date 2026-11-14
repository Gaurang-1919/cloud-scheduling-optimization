import os
import shutil

main_tex_path = r"C:\Users\gaurang\PycharmProjects\cloud_scheduling_project\paper\main.tex"
with open(main_tex_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace placeholders with Gaurang's exact real credentials
content = content.replace("gaurang.uit@gmail.com", "gaurang.ug24@nsut.ac.in")
content = content.replace("https://github.com/gaurang-uit/cloud-scheduling-optimization", "https://github.com/Gaurang-1919/cloud-scheduling-optimization")
content = content.replace(r"\affil*[1]{\orgdiv{Department of Information Technology}, \orgname{Course: Cloud Computing (Roll Nos: 2024UIT3048, 2024UIT3033)}, \orgaddress{\city{New Delhi}, \postcode{110078}, \country{India}}}",
                          r"\affil*[1]{\orgdiv{Department of Information Technology}, \orgname{Netaji Subhas University of Technology (NSUT)}, \orgaddress{\street{Sector 3, Dwarka}, \city{New Delhi}, \postcode{110078}, \country{India}}}")

with open(main_tex_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated main.tex with NSUT affiliation and Gaurang-1919 GitHub link.")

# Also update generate_paper_pdf.py
pdf_script = r"C:\Users\gaurang\PycharmProjects\cloud_scheduling_project\paper\generate_paper_pdf.py"
with open(pdf_script, 'r', encoding='utf-8') as f:
    pcontent = f.read()

pcontent = pcontent.replace("gaurang.uit@gmail.com", "gaurang.ug24@nsut.ac.in")
pcontent = pcontent.replace("https://github.com/gaurang-uit/cloud-scheduling-optimization", "https://github.com/Gaurang-1919/cloud-scheduling-optimization")
pcontent = pcontent.replace("Course: Cloud Computing (Roll Nos: 2024UIT3048, 2024UIT3033), New Delhi, 110078, India",
                            "Netaji Subhas University of Technology (NSUT), Dwarka, New Delhi 110078, India (Roll Nos: 2024UIT3048, 2024UIT3033)")

with open(pdf_script, 'w', encoding='utf-8') as f:
    f.write(pcontent)

print("Updated generate_paper_pdf.py.")
