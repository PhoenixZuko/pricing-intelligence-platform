import csv
import os
import yaml
import re
import glob


# Caută folderul părinte care începe cu results_data_
parent_dir = os.path.abspath(os.path.join(os.getcwd(), ".."))
result_dirs = [d for d in os.listdir(parent_dir) if d.startswith("results_data_") and os.path.isdir(os.path.join(parent_dir, d))]

if not result_dirs:
    raise FileNotFoundError("No folder starting with 'results_data_' found in parent directory.")

target_dir = os.path.join(parent_dir, result_dirs[0])
output_csv = os.path.join(target_dir, "output_data_with_category.csv")
input_csv = "output_data_with_type.csv"
dictionary_folder = "type_definitions"

# Citește toate fișierele YAML din folder
yaml_files = [f for f in os.listdir(dictionary_folder) if f.startswith("type_") and f.endswith(".yml")]

# Încarcă regulile pe baza fiecărui tip
type_rules = {}

for file in yaml_files:
    type_name = file[len("type_"):-len(".yml")].strip().lower()
    with open(os.path.join(dictionary_folder, file), "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
        type_rules[type_name] = data.get("categories", [])

def clean_word(word):
    return re.sub(r'[^a-zA-ZäöüÄÖÜß0-9]', '', word.lower())

def find_category_and_subcategory(product, categories_data):
    original_words = product.split()
    cleaned_words = [clean_word(w) for w in original_words]

    for entry in categories_data:
        category = entry.get("category", "").strip()
        synonyms = entry.get("synonyms", [])

        for synonym in synonyms:
            synonym_clean = clean_word(synonym)
            if synonym_clean in cleaned_words:
                index = cleaned_words.index(synonym_clean)
                rest = original_words[index + 1:]
                subcat = " ".join(rest).strip(" -–():")
                return category, subcat if subcat else "general"
    return None, None

def fix_unmatched_parentheses(text):
    if not text:
        return text
    open_count = text.count('(')
    close_count = text.count(')')
    if open_count > close_count:
        text += ')' * (open_count - close_count)
    elif close_count > open_count:
        text = '(' * (close_count - open_count) + text
    return text

def normalize_subcategory_text(text):
    if not text:
        return text

    # Conversii numerale romane în cifre arabe
    replacements = {
        'AⅠ–AⅢ': 'A1-A3',
        'AⅠ':'A1',
        'AⅡ':'A2',
        'AⅢ':'A3',
        'AⅣ':'A4',
        'AⅤ':'A5',
        'AⅥ':'A6',
        'AⅦ':'A7',
        'AⅧ':'A8',
        'AⅨ':'A9',
        'AⅩ':'A10',
    }

    for key, value in replacements.items():
        text = text.replace(key, value)

    # Elimină simbolul "–" (en dash)
    text = text.replace("–", " ")

    # Elimină slash de început: "/ Bauglas" → "Bauglas"
    text = re.sub(r'^\s*/\s*', '', text)

    # Curăță spații multiple
    text = re.sub(r'\s{2,}', ' ', text)

    return text.strip()


# Procesare CSV
with open(input_csv, newline='', encoding='utf-8') as csvfile_in, \
     open(output_csv, 'w', newline='', encoding='utf-8') as csvfile_out:

    reader = csv.DictReader(csvfile_in)
    fieldnames = reader.fieldnames + ["category", "subcategory"]
    writer = csv.DictWriter(csvfile_out, fieldnames=fieldnames)
    writer.writeheader()

    for row in reader:
        type_value = row.get("type", "").strip().lower()
        if type_value in type_rules:
            category, subcategory = find_category_and_subcategory(row["produkt"], type_rules[type_value])
            if category:
                row["category"] = category
                subcategory = normalize_subcategory_text(subcategory)
                row["subcategory"] = fix_unmatched_parentheses(subcategory)
        writer.writerow(row)
