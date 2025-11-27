import os
import re
import csv

folder_path = "results_clearago"
output_file = os.path.join(folder_path, "clearago_final.csv")

def process_price(price_str):
    # Procesăm prețul: eliminăm simbolul euro și transformăm într-un număr
    price_str = price_str.replace(",", ".").strip()
    try:
        price_float = float(price_str)
        return price_float
    except ValueError:
        return None

def extract_data_from_file(filepath):
    with open(filepath, "r", encoding="utf-8") as file:
        content = file.read()

    postal_match = re.search(r"Ihre Auswahl:\s*(\d{5})", content)
    postalcode = postal_match.group(1) if postal_match else ""

    category_match = re.search(r"Ihre Auswahl:\s*\d{5}\s+(.+)", content)
    category = category_match.group(1).strip() if category_match else ""

    subcategory_match = re.search(r"m³\s+(.*?)\s+in\s+\d{5}", content)
    subcategory = subcategory_match.group(1).strip() if subcategory_match else ""

    # Extragem toate intrările de tipul (număr m³, preț)
    entries = re.findall(r"(\d{1,2},\d{0,1})m³\s*[\w\s()<>%\-]*?\s*?(\d{2,4},\d{2})\s?€", content)

    results = []
    for größe_str, preis_str in entries:
        größe = größe_str.replace(",", ".")
        preis = f"{preis_str} €"
        preis_numerisch = process_price(preis_str)

        if preis_numerisch is None or preis_numerisch == 0:
            continue  # Ignorăm produsele cu preț invalid sau 0

        product_name = f"{category} / {subcategory}"

        results.append([product_name, subcategory, größe, preis, preis_numerisch, postalcode])

    return results

all_data = []
for filename in sorted(os.listdir(folder_path)):
    if filename.endswith(".txt"):
        filepath = os.path.join(folder_path, filename)
        all_data.extend(extract_data_from_file(filepath))

# Scriem datele într-un fișier CSV
with open(output_file, "w", encoding="utf-8", newline="") as csvfile:
    writer = csv.writer(csvfile, delimiter=";")
    writer.writerow(["produkt", "subprodukt", "größe", "preis", "preis_numerisch", "postalcode"])
    writer.writerows(all_data)

print(f"✔️ CSV generat cu succes: {output_file}")
