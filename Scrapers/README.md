# Scrapers Module

This folder contains all the web scrapers and data formatters used in the project.  
Each scraper is dedicated to a specific source, while additional scripts handle CSV/JSON output formatting.

---

## 🔹 Structure

- **core_clearago/**  
  Contains helper functions and logic specific to the Clearago source.

- **core_ensorgo/**  
  Contains helper functions and logic specific to the Ensorgo source.

- **1cdz-scraper.py**  
  Scraper for source **CDZ**.

- **2dino-scraper.py**  
  Scraper for source **Dino**.

- **3klebs-scraper.py**  
  Scraper for source **Klebs**.

- **4main_clearago.py**  
  Scraper entrypoint for **Clearago**.

- **5main_ensorgo.py**  
  Scraper entrypoint for **Ensorgo**.

- **cvs_maker.py**  
  Collects temporary scraped results and generates a final **CSV file**.

- **json_maker.py**  
  Collects temporary scraped results and generates a final **JSON file**.

---

## 🔹 Workflow
1. Each scraper (`*-scraper.py`) runs independently and extracts data from its source.  
2. The scraped results are stored temporarily.  
3. `cvs_maker.py` and `json_maker.py` process the collected results and produce properly formatted output files.  
   - **CSV format**: `output_data.csv`  
   - **JSON format**: `output_data.json`  

---

## 🔹 Notes
- Scrapers are modular: you can activate/deactivate them individually.  
- Temporary files are automatically cleaned up by `cleaner.py` after processing.  
- The output is stored in folders like:  
