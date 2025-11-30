import tkinter as tk
from tkinter import font
import pathlib
import urllib.request
import zipfile
import os

# ------------------- SETUP -------------------
BASE_DIR = pathlib.Path(__file__).parent.resolve()
FONTS_DIR = BASE_DIR / "fonts"
FONTS_DIR.mkdir(exist_ok=True)

# Font name → (download_url, filename_inside_zip_or_direct, final_local_name)
FONTS = {
    "IBM Plex Sans": (
        "https://github.com/IBM/plex/releases/download/v7.3.0/IBM-Plex-Sans.zip",
        "fonts/ttf/IBMPlexSans-Regular.ttf",
        "IBMPlexSans-Regular.ttf"
    ),
    "Spectral": (
        "https://github.com/productiontype/Spectral/releases/download/2.009/Spectral-2.009.zip",
        "Spectral-Regular.ttf",
        "Spectral-Regular.ttf"
    ),
    "Manrope": (
        "https://github.com/sharanda/manrope/releases/download/v8.0.0/manrope.zip",
        "fonts/ttf/static/Manrope-Regular.ttf",
        "Manrope-Regular.ttf"
    ),
    "Satoshi": (
        "https://cdn.satoshi-font.com/Satoshi-Regular.ttf",  # direct link
        None,  # no zip
        "Satoshi-Regular.ttf"
    ),
    "Crimson Pro": (
        "https://github.com/googlefonts/crimsonpro/raw/main/fonts/variable/CrimsonPro%5Bwght%5D.ttf",
        None,  # direct variable font
        "CrimsonPro[wght].ttf"
    ),
}

# ------------------- DOWNLOAD & EXTRACT -------------------
def ensure_font(family, url, inner_path, local_name):
    target = FONTS_DIR / local_name
    
    if target.exists():
        return target  # already have it
    
    print(f"Downloading {family}...")
    tmp_zip = FONTS_DIR / f"{family.replace(' ', '_')}_temp.zip"
    
    try:
        urllib.request.urlretrieve(url, tmp_zip)
        print(f"   Downloaded {family}")
        
        if inner_path is None:  # direct .ttf file
            os.rename(tmp_zip, target)
        else:  # it's a zip
            with zipfile.ZipFile(tmp_zip, 'r') as z:
                if inner_path in z.namelist():
                    z.extract(inner_path, FONTS_DIR)
                    extracted = FONTS_DIR / inner_path
                    extracted.rename(target)
                else:
                    print(f"   Could not find {inner_path} in zip")
            tmp_zip.unlink()
        print(f"   Ready: {local_name}")
    except Exception as e:
        print(f"   Failed {family}: {e}")
        if tmp_zip.exists():
            tmp_zip.unlink()
        return None
    return target

# ------------------- LOAD INTO TKINTER -------------------
def load_all_fonts(root):
    loaded = 0
    for family, (url, inner, local) in FONTS.items():
        path = ensure_font(family, url, inner, local)
        if path and path.exists():
            try:
                root.tk.call("font", "create", family, "-family", str(path))
                loaded += 1
            except Exception as e:
                print(f"   Could not register {family}: {e}")
    print(f"\nSuccessfully loaded {loaded} out of 5 fonts!\n")

# ------------------- GUI -------------------
root = tk.Tk()
root.title("5 Beautiful Fonts — Ready to Use")
root.geometry("1100x800")
root.configure(bg="#fafafa")

load_all_fonts(root)

tk.Label(root, text="Pick Your Favorite Professional Font", 
         font=("Segoe UI", 24, "bold"), bg="#fafafa", fg="#222").pack(pady=30)

sample = "The quick brown fox jumps over the lazy dog.\n1234567890 — Professional, artful, and readable."

for family in FONTS.keys():
    frame = tk.Frame(root, bg="white", relief="solid", bd=1, padx=20, pady=20)
    frame.pack(fill="x", padx=50, pady=12)
    
    tk.Label(frame, text=family, font=("Segoe UI", 16, "bold"), bg="white", anchor="w").pack(anchor="w")
    tk.Label(frame, text=sample, font=(family, 18), bg="white", fg="#111", justify="left", wraplength=1000).pack(anchor="w", pady=8)

tk.Label(root, text="All fonts downloaded & loaded privately — no installation needed", 
         font=("Segoe UI", 11), fg="#666", bg="#fafafa").pack(pady=30)

root.mainloop()