import asyncio
import os
import re
import csv
from datetime import datetime
from playwright.async_api import async_playwright


async def scrape_dino():
    results = []
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        await page.goto("https://www.dino-container.de/preise-containerdienst-berlin/preise-container/", timeout=60000)

        # Accept cookies
        try:
            await page.click("button#CookieBoxSaveButton", timeout=5000)
        except:
            pass  # Dacă nu apare, ignoră

        await page.wait_for_selector("div.berlin-container table")

        rows = await page.query_selector_all("div.berlin-container table tbody tr")
        for row in rows:
            try:
                cells = await row.query_selector_all("td")
                if len(cells) < 2:
                    continue

                cell_text = await cells[0].text_content()
                price_text = await cells[1].text_content()

                match = re.search(r"(\d+)\s*(cbm|m³)?\s*(.*)", cell_text)
                if not match:
                    continue

                volume = match.group(1).strip()
                unit = match.group(2).strip() if match.group(2) else "m³"
                product = match.group(3).strip()

                price_match = re.search(r"(\d{1,3}(?:\.\d{3})*,\d{2})", price_text)
                if not price_match:
                    continue

                price = price_match.group(1)
                price_number = float(price.replace('.', '').replace(',', '.'))

                results.append({
                    "produkt": product,
                    "größe": volume,
                    "preis": f"{price} €",
                    "preis_numerisch": price_number,
                    "kontext": price_text.strip(),
                    "fehler": ""
                })

                print(f"✅ {volume} {unit} | {product} | {price} €")

            except Exception as e:
                print(f"❌Processing error: {e}")

        await browser.close()

    # Salvare CSV
    if results:
        os.makedirs("results_dino_container", exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"results_dino_container/dino_container_{timestamp}.csv"
        with open(filename, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=results[0].keys())
            writer.writeheader()
            writer.writerows(results)
        print(f"\n✅ Complete save in: {filename}")
    else:
        print("⚠️No lines saved")


if __name__ == "__main__":
    asyncio.run(scrape_dino())
