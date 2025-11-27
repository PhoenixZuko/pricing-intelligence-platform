import asyncio
from datetime import datetime
import csv
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from core_ensorgo.scraper import run_scraper

async def main():
    print("🚀 I start the entsorgho scraper...")
    results = await run_scraper()

    if not results:
        print("⚠️ No results found.")
        return

    print(f"⏳ Saving {len(results)} results to file...")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"entsorgo_results_{timestamp}.csv"

    os.makedirs("results_ensorgo", exist_ok=True)
    filepath = os.path.join("results_ensorgo", filename)

    # 🧱 Asigură ordinea exactă a coloanelor
    fieldnames = ["produkt", "größe", "preis", "preis_numerisch", "kontext", "fehler"]

    try:
        with open(filepath, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(results)
        print(f"✅ Results successfully saved in: {filepath}")
    except Exception as e:
        print(f"❌ Error saving: {e}")

if __name__ == "__main__":
    asyncio.run(main())
