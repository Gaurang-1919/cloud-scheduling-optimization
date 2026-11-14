import os

overleaf_url = "https://www.overleaf.com/project/6af89462a6b4fbf99f1afded/share#d1d42196d4c6c82f2e81aac36419c0ccbbd0d131f858b99e"
github_url = "https://github.com/Gaurang-1919/cloud-scheduling-optimization"

# 1. Update main.tex
main_tex_path = r"C:\Users\gaurang\PycharmProjects\cloud_scheduling_project\paper\main.tex"
with open(main_tex_path, 'r', encoding='utf-8') as f:
    tex = f.read()

# Replace any broken overleaf url in main.tex with a clean \href
old_decl_tex = r"\item \textbf{Data, Code, and Overleaf Workspace Availability:} All simulation scripts, benchmark datasets, neural model weights, and presentation materials are publicly available in our GitHub repository: \url{https://github.com/Gaurang-1919/cloud-scheduling-optimization}. Furthermore, the complete Springer Nature LaTeX manuscript workspace is accessible via Overleaf: \url{https://www.overleaf.com/project/6af89462a6b4fbf99f1afded/share#d1d42196d4c6c82f2e81aac36419c0ccbbd0d131f858b99e}."

new_decl_tex = r"\item \textbf{Data, Code, and Overleaf Workspace Availability:} All simulation scripts, benchmark datasets, neural model weights, and presentation materials are publicly available in our GitHub repository: \url{https://github.com/Gaurang-1919/cloud-scheduling-optimization}. Furthermore, the complete Springer Nature LaTeX live authoring workspace is accessible on Overleaf: \href{" + overleaf_url + r"}{Overleaf Live Workspace}."

if old_decl_tex in tex:
    tex = tex.replace(old_decl_tex, new_decl_tex)
else:
    # replace any url matching
    import re
    tex = re.sub(r'\\url\{https://www\.overleaf\.com/project/6af89462a6b4fbf99f1afded/share[^}]*\}',
                 r'\\href{' + overleaf_url + r'}{Overleaf Live Workspace}', tex)

with open(main_tex_path, 'w', encoding='utf-8') as f:
    f.write(tex)

print("Updated main.tex with clickable href.")

# 2. Update generate_paper_pdf.py
pdf_script = r"C:\Users\gaurang\PycharmProjects\cloud_scheduling_project\paper\generate_paper_pdf.py"
with open(pdf_script, 'r', encoding='utf-8') as f:
    ptext = f.read()

# Replace the Page 1 author affiliation line with clickable hyperlink
old_affil = 'Overleaf Workspace: https://www.overleaf.com/project/6af89462a6b4fbf99f1afded/share#d1d42196d4c6c82f2e81aac36419c0ccbbd0d131f858b99e'
new_affil = 'Overleaf Workspace: <font color="#1d4ed8"><a href="' + overleaf_url + '"><u>Overleaf Live Workspace (Click Here)</u></a></font>'
ptext = ptext.replace(old_affil, new_affil)

# Replace the Declarations line with clean clickable hyperlink that never breaks across lines
old_decl_pdf = 'The complete Springer Nature LaTeX manuscript and live editing workspace are also hosted on Overleaf at: <u>https://www.overleaf.com/project/6af89462a6b4fbf99f1afded/share#d1d42196d4c6c82f2e81aac36419c0ccbbd0d131f858b99e</u>.'
new_decl_pdf = 'The complete Springer Nature LaTeX manuscript and live editing workspace are also hosted on Overleaf at: <font color="#1d4ed8"><a href="' + overleaf_url + '"><u>Overleaf Live Workspace (Click to Open)</u></a></font>.'
ptext = ptext.replace(old_decl_pdf, new_decl_pdf)

# Also ensure any raw occurrence is replaced
import re
ptext = re.sub(r'<u>https://www\.overleaf\.com/project/6af89462a6b4fbf99f1afded/share#[^<]*</u>',
               '<font color="#1d4ed8"><a href="' + overleaf_url + '"><u>Overleaf Live Workspace (Click to Open)</u></a></font>',
               ptext)

with open(pdf_script, 'w', encoding='utf-8') as f:
    f.write(ptext)

print("Updated generate_paper_pdf.py with clickable links.")
