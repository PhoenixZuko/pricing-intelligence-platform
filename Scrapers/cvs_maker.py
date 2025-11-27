import json
import csv
import re
from urllib.parse import urlparse
import shutil
import os
# Încarcă fișierul JSON
with open('output_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Funcție pentru a obține doar domeniul fără "https://" și "/"
def get_domain(url):
    parsed_url = urlparse(url)
    return parsed_url.netloc  # Returnează doar domeniul

# Funcție pentru a curăța prețul
# Funcție pentru a curăța prețul
def clean_price(price_str):
    if isinstance(price_str, str):  # Verifică dacă prețul este un șir
        price_clean = price_str.replace(".", "").replace(",", ".").strip()  # Se înlocuiește virgula cu punct
        try:
            return float(price_clean)
        except ValueError:
            return None  # Dacă nu e un preț valid, returnează None
    elif isinstance(price_str, (int, float)):  # Dacă este deja număr, îl returnează
        return float(price_str)
    else:
        return None  # În caz că prețul nu e valid


# Funcție pentru a curăța textul din câmpul "produkt"
def clean_product_name(product_name):
    # Eliminăm "cbm (kubikmeter)" și "– container" din text
    product_name = re.sub(r"(\d+,\d+|\d+)\s*cbm\s*\(kubikmeter\)", "", product_name)  # Curăță „cbm (kubikmeter)”
    product_name = product_name.replace("– container", "").strip()  # Curăță „– container”
    return product_name

# Pregătește datele pentru CSV
csv_data = []
header = ["date", "link", "kubikmeter", "produkt", "currency", "price"]

# Parcurge toate site-urile din JSON
for site, site_data in data.items():
    date = site_data["data_extraction"]
    for product_name, product_list in site_data["products"].items():
        for product in product_list:
            kubikmeter = product["cbm"]
            price = product["price"]
            currency = product["currency"]
            
            # Curățăm prețul
            price_numeric = clean_price(price)
            if price_numeric is None:
                continue  # Dacă prețul nu e valid, îl sărim

            # Curățăm numele produsului
            clean_name = clean_product_name(product_name)

            # Extragem doar domeniul din link
            domain = get_domain(site)
            
            # Adăugăm rândul în lista finală
            csv_data.append([date, domain, kubikmeter, clean_name, currency, price_numeric])

# Salvează datele în CSV
output_file = "output_data.csv"
with open(output_file, mode='w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(csv_data)

print(f"✅ Final CSV saved: {output_file}")

print(f"✅ Final CSV saved: {output_file}")


# Liste de foldere de șters
folders_to_delete = [
    "results_cdz-berlin",
    "results_clearago",
    "results_dino_container",
    "results_ensorgo",
    "results_klebs"
]

# Șterge fiecare folder dacă există
for folder in folders_to_delete:
    if os.path.exists(folder) and os.path.isdir(folder):
        try:
            shutil.rmtree(folder)
            print(f"[DELETED] Folder deleted: {folder}")
        except Exception as e:
            print(f"[ERROR] Failed to delete {folder}: {e}")
    else:
        print(f"[SKIPPED] Folder not found: {folder}")
from datetime import datetime

try:
    # Data curentă în format DD_MM_YYYY
    date_str = datetime.now().strftime("%d_%m_%Y")

    # Folderul: ../results_data_DD_MM_YYYY
    parent_dir = os.path.abspath(os.path.join(os.getcwd(), ".."))
    results_dir = os.path.join(parent_dir, f"results_data_{date_str}")

    # 🔁 Dacă există, șterge tot
    if os.path.exists(results_dir):
        shutil.rmtree(results_dir)
        print(f"[CLEANED] Existing folder removed: {results_dir}")

    # Creează din nou
    os.makedirs(results_dir)

    # Fișierele de mutat (nume rămân neschimbate)
    files_to_move = ["output_data.csv", "output_data.json"]
    for file in files_to_move:
        if os.path.exists(file):
            dst = os.path.join(results_dir, file)  # păstrează numele original
            shutil.move(file, dst)
            print(f"[MOVED] {file} → {dst}")
        else:
            print(f"[SKIPPED] {file} not found in current folder.")

except Exception as e:
    print(f"[ERROR] Moving files failed: {e}")
