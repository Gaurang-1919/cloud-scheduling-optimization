import os
import zipfile
import shutil

source_dir = r"C:\Users\gaurang\PycharmProjects\cloud_scheduling_project\paper"
zip_path_project = r"C:\Users\gaurang\PycharmProjects\cloud_scheduling_project\paper\Springer_Nature_Research_Paper.zip"
zip_path_desktop = r"C:\Users\gaurang\OneDrive\Desktop\Springer_Nature_Research_Paper.zip"

files_to_include = [
    "main.tex",
    "references.bib",
    "sn-jnl.cls",
    "sn-mathphys-num.bst",
    "sn-basic.bst",
    "sn-aps.bst",
    "sn-nature.bst"
]

fig_dir = os.path.join(source_dir, "figures")
figures = [f for f in os.listdir(fig_dir) if f.endswith(".png")]

with zipfile.ZipFile(zip_path_project, "w", zipfile.ZIP_DEFLATED) as zf:
    for f in files_to_include:
        fp = os.path.join(source_dir, f)
        if os.path.exists(fp):
            zf.write(fp, arcname=f)
            
    for fig in figures:
        fp = os.path.join(fig_dir, fig)
        zf.write(fp, arcname=f"figures/{fig}")

print(f"Created project zip: {zip_path_project} ({os.path.getsize(zip_path_project)} bytes)")

# Copy to Desktop
shutil.copy2(zip_path_project, zip_path_desktop)
print(f"Copied zip to Desktop: {zip_path_desktop}")
