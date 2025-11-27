import subprocess
import os
import yaml

# === 1. Configurează cronjob-ul ===
import os
import subprocess

def ensure_cronjob():
    import subprocess, os
    interval_days = int(os.getenv("SCRAPER_SCHEDULE", "7"))
    runner_path = os.path.abspath(__file__)
    cron_line = f"0 2 */{interval_days} * * /usr/bin/python3 {runner_path} >> /tmp/runner.log 2>&1"

    current_cron = subprocess.getoutput("crontab -l || true").splitlines()
    filtered_cron = [line for line in current_cron if "runner.py" not in line]

    new_cron = "\n".join(filtered_cron + [cron_line]) + "\n"
    subprocess.run("crontab -", input=new_cron.encode(), shell=True, check=True)
    print(f"📌 Cronjob reset: every {interval_days} days at 02:00.")

# === 2. Rulează runner-ul normal ===
def run_scrapers():
    scraper_folder = "Scrapers"

    # Încarcă configurarea din config.yaml
    config_path = os.path.join(os.path.dirname(__file__), "config.yaml")
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    # Rulează doar scripturile active definite în YAML
    for entry in config["scrapers"]:
        if not entry.get("enabled", False):
            continue

        script = entry["script"]
        print(f"\n Now Running: {script}")
        try:
            subprocess.run(["python3", script], cwd=scraper_folder, check=True)
            print(f" Successful completion: {script}")
        except subprocess.CalledProcessError as e:
            print(f" Error running {script}: {e}")

    # Rulează scripturile standard (json & csv)
    standard_scripts = ["json_maker.py", "cvs_maker.py"]

    for script in standard_scripts:
        print(f"\n Finalizing: {script}")
        try:
            subprocess.run(["python3", script], cwd=scraper_folder, check=True)
            print(f" Done: {script}")
        except subprocess.CalledProcessError as e:
            print(f" Error in {script}: {e}")

    # Rulează scripturile din category_parser
    category_scripts = ["create_type.py", "create_category.py"]

    for script in category_scripts:
        print(f"\n Running category parser: {script}")
        try:
            subprocess.run(["python3", script], cwd="category_parser", check=True)
            print(f" Category script completed: {script}")
        except subprocess.CalledProcessError as e:
            print(f" Error in category parser script {script}: {e}")

    # Rulează scriptul de setup DB
    print("\n Importing data into PostgreSQL...")
    try:
        subprocess.run(["python3", "db_setup.py"], cwd="database", check=True)
        print(" Database populated successfully.")
    except subprocess.CalledProcessError as e:
        print(f" Error importing data to database: {e}")

    # Rulează cleaner.py
    print("\n Running cleaner script...")
    try:
        subprocess.run(["python3", "cleaner.py"], cwd="utils", check=True)
        print(" Cleaner finished successfully.")
    except subprocess.CalledProcessError as e:
        print(f" Error running cleaner script: {e}")


if __name__ == "__main__":
    run_scrapers()     # rulează imediat
