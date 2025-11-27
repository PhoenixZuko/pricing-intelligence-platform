import os
import csv
import json
from datetime import datetime

# Mapping foldere -> site
folders_info = {
    "results_cdz-berlin": "https://cdz-berlin.de/shop",
    "results_clearago": "https://www.clearago.de/",
    "results_klebs": "https://www.klebs.info/",
    "results_dino_container": "https://www.dino-container.de/",
    "results_ensorgo": "https://app.entsorgo.de"
}

def find_latest_csv(folder_path):
    csv_files = [f for f in os.listdir(folder_path) if f.endswith(".csv")]
    if not csv_files:
        return None, None
    csv_files = sorted(csv_files, key=lambda f: os.path.getmtime(os.path.join(folder_path, f)), reverse=True)
    latest_file = csv_files[0]
    latest_path = os.path.join(folder_path, latest_file)
    file_time = os.path.getmtime(latest_path)
    extraction_time = datetime.fromtimestamp(file_time).strftime('%Y-%m-%d %H:%M:%S')
    return latest_path, extraction_time

def detect_separator(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        first_line = file.readline()
        if ',' in first_line:
            return ','
        elif ';' in first_line:
            return ';'
        else:
            return ','  # Default to comma if we can't detect

def process_price(price_str):
    # Curățăm prețul de simboluri și transformăm într-un număr
    price_str = price_str.replace(",", ".").replace("€", "").strip()
    try:
        price_float = float(price_str)
        return price_float
    except ValueError:
        return None

def read_csv_grouped_by_product(file_path):
    data = {}
    separator = detect_separator(file_path)  # Detectăm separatorul utilizat în fișier
    print(f"📂 We read the file: {file_path} with separator '{separator}'")

    with open(file_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=separator)
        
        for row in reader:
            print(f"🔍 We read the line: {row}")  # Debugging pentru fiecare rând citit
            
            # Dacă avem ambele coloane (produkt și subprodukt), luam doar subprodukt
            name = f"{row.get('subprodukt', '').strip()}"
            if not name:  # Dacă subproduktul este gol, folosim produkt
                name = f"{row.get('produkt', '').strip()}"

            cbm = row['größe'].strip()
            price_raw = row['preis'].strip()

            # Detectăm valuta
            currency = '€' if '€' in price_raw else ''
            price_num = price_raw.replace('€', '').replace(' EUR', '').replace(',', '.').strip()
            price_float = process_price(price_num)

            if price_float is None or price_float == 0:
                continue  # Ignorăm produsele cu preț invalid sau 0

            if name not in data:
                data[name] = []

            data[name].append({
                "cbm": cbm,
                "price": price_float,
                "currency": currency
            })

    return data

# Rezultatul final
final_json = {}

for folder, site_url in folders_info.items():
    if not os.path.exists(folder):
        print(f"⚠️ The folder does not exist: {folder}")
        continue

    csv_path, extraction_time = find_latest_csv(folder)
    if not csv_path:
        print(f"⚠️ No CSV files found in: {folder}")
        continue

    print(f"📂 We read from: {csv_path}")
    grouped_data = read_csv_grouped_by_product(csv_path)

    final_json[site_url] = {
        "data_extraction": extraction_time,
        "products": grouped_data
    }

# Salvăm JSON-ul final
with open("output_data.json", "w", encoding="utf-8") as f:
    json.dump(final_json, f, ensure_ascii=False, indent=2)

print("\n✅ Final JSON saved: output_data.json")
