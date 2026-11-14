import os

main_tex = r"C:\Users\gaurang\PycharmProjects\cloud_scheduling_project\paper\main.tex"
with open(main_tex, 'r', encoding='utf-8') as f:
    text = f.read()

# Fix Documentclass
text = text.replace(r"\documentclass[sn-mathphys-num]{sn-jnl}", r"\documentclass[default,sn-mathphys-num]{sn-jnl}")

# Fix Preamble packages
old_preamble = r"""\usepackage{graphicx}
\usepackage{multirow}
\usepackage{amsmath,amssymb,amsfonts}
\usepackage{amsthm}
\usepackage{mathrsfs}
\usepackage[title]{appendix}
\usepackage{xcolor}
\usepackage{textcomp}
\usepackage{manyfoot}
\usepackage{booktabs}
\usepackage{algorithm}
\usepackage{algorithmicx}
\usepackage{algpseudocode}
\usepackage{listings}
\usepackage{url}
\usepackage{subcaption}"""

new_preamble = r"""\usepackage{graphicx}
\usepackage{multirow}
\usepackage{amsmath,amssymb,amsfonts}
\usepackage{mathrsfs}
\usepackage[title]{appendix}
\usepackage{xcolor}
\usepackage{textcomp}
\usepackage{manyfoot}
\usepackage{booktabs}
\usepackage{algorithm}
\usepackage{algorithmicx}
\usepackage{algpseudocode}
\usepackage{listings}
\usepackage{url}

\theoremstyle{thmstyleone}
\newtheorem{theorem}{Theorem}
\newtheorem{proposition}[theorem]{Proposition}
\theoremstyle{thmstyletwo}
\newtheorem{example}{Example}
\newtheorem{remark}{Remark}
\theoremstyle{thmstylethree}
\newtheorem{definition}{Definition}"""

if old_preamble in text:
    text = text.replace(old_preamble, new_preamble)
    print("Replaced preamble successfully.")
else:
    print("Exact old preamble not matched, checking with normalized newlines...")
    old_p_norm = old_preamble.replace("\r\n", "\n")
    text_norm = text.replace("\r\n", "\n")
    if old_p_norm in text_norm:
        text = text_norm.replace(old_p_norm, new_preamble.replace("\r\n", "\n"))
        print("Replaced normalized preamble successfully.")

# Replace Overleaf URL with the official working Springer template link
text = text.replace(
    r"\url{https://www.overleaf.com/project/cloud-scheduling-optimization}",
    r"\url{https://www.overleaf.com/latex/templates/springer-nature-latex-template/gsvvftmrppwq}"
)
text = text.replace(
    r"https://www.overleaf.com/project/cloud-scheduling-optimization",
    r"https://www.overleaf.com/latex/templates/springer-nature-latex-template/gsvvftmrppwq"
)

with open(main_tex, 'w', encoding='utf-8') as f:
    f.write(text)

print("Updated main.tex with official Overleaf compatibility fixes.")

# Also update generate_paper_pdf.py
pdf_script = r"C:\Users\gaurang\PycharmProjects\cloud_scheduling_project\paper\generate_paper_pdf.py"
with open(pdf_script, 'r', encoding='utf-8') as f:
    ptext = f.read()

ptext = ptext.replace(
    "https://www.overleaf.com/project/cloud-scheduling-optimization",
    "https://www.overleaf.com/latex/templates/springer-nature-latex-template/gsvvftmrppwq"
)

with open(pdf_script, 'w', encoding='utf-8') as f:
    f.write(ptext)

print("Updated generate_paper_pdf.py.")
