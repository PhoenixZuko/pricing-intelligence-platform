import asyncio
import os
import subprocess
from core_clearago.homepage import launch_browser_and_submit_postcode
from core_clearago.waste_categories import browse_waste_categories

# === Config ===
HEADLESS = True
PAUSE_ON_END = False
POSTCODE = "10117"
RESULTS_FOLDER = "results_clearago"

async def main():
    print(f"[🚀] Starting Clearago Scraper (debug mode: {not HEADLESS})")

    # Creează folderul de rezultate dacă nu există
    os.makedirs(RESULTS_FOLDER, exist_ok=True)

    # === PASUL 1: Deschide pagina principală și trimite codul poștal ===
    print("[1] Opening site and submitting postcode...")
    page = await launch_browser_and_submit_postcode(
        postcode=POSTCODE,
        headless=HEADLESS,
        pause_on_end=False,
        return_page=True
    )

    # === PASUL 2: Caută și salvează categoriile de deșeuri ===
    await browse_waste_categories(page, results_folder=RESULTS_FOLDER)

    # === Închide browserul și contextul ===
    try:
        await page.context.close()
        await page.context.browser.close()
    except Exception as e:
        print(f"[⚠️] Error during browser shutdown: {e}")

    print("[📁] Running CSV formatter...")

    # === PASUL 3: Rulează format_csv.py ===
    try:
        subprocess.run(["python3", "core_clearago/format_csv.py"], check=True)
        print("[✅] CSV final generat cu succes.")
    except Exception as e:
        print(f"[❌] Eroare la rularea format_csv.py: {e}")

    print("[🏁] Finished Clearago scraping and CSV export.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except RuntimeError as e:
        if "Event loop is closed" in str(e):
            print("[⚠️] RuntimeWarning: Event loop was already closed.")
