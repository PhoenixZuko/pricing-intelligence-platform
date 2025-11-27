import csv
import yaml
import re
import os
import glob

def find_input_file():
    parent_dir = os.path.abspath(os.path.join(os.getcwd(), ".."))
    result_dirs = [d for d in os.listdir(parent_dir) if d.startswith("results_data_") and os.path.isdir(os.path.join(parent_dir, d))]

    if not result_dirs:
        raise FileNotFoundError("No folder starting with 'results_data_' found in parent directory.")

    # Poți alege primul folder găsit (sau adaugă sortare dacă e nevoie)
    target_dir = os.path.join(parent_dir, result_dirs[0])
    input_csv_path = os.path.join(target_dir, "output_data.csv")

    if not os.path.isfile(input_csv_path):
        raise FileNotFoundError(f"'output_data.csv' not found in {target_dir}")

    return input_csv_path


# Citim expresiile din YAML
def load_type_dictionary(path='type_definitions/type.yaml'):
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

# Detectăm tipul (type) pe baza cuvintelor cheie – cuvânt întreg, insensibil la majuscule
def detect_type(product_name, type_dict):
    text = product_name.lower().replace('-', ' ').replace('"', '')
    words = text.split()
    for type_name, keywords in type_dict.items():
        for keyword in keywords:
            keyword_lower = keyword.lower()
            # Dacă e expresie din mai multe cuvinte
            if ' ' in keyword_lower:
                if keyword_lower in text:
                    return type_name
            else:
                # Dacă e cuvânt unic, verificăm ca să fie izolat (ex: "holz" să nu prindă "Altholz")
                if re.search(rf'(?<!\w){re.escape(keyword_lower)}(?!\w)', text):
                    return type_name
    return "Other"

# Procesăm CSV-ul original și adăugăm coloana 'type'
def process_file(input_csv, output_csv='output_data_with_type.csv', yaml_path='type_definitions/type.yaml'):
    type_dict = load_type_dictionary(yaml_path)

    with open(input_csv, 'r', encoding='utf-8') as infile, \
         open(output_csv, 'w', encoding='utf-8', newline='') as outfile:

        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames[:]
        if 'type' not in fieldnames:
            fieldnames.insert(1, 'type')  # inserăm după 'date'

        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            product = row.get('produkt', '')
            row['type'] = detect_type(product, type_dict)
            writer.writerow(row)

# Rulează scriptul
if __name__ == "__main__":
    input_file_path = find_input_file()
    process_file(input_csv=input_file_path)

