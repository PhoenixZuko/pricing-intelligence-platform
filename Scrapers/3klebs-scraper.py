import asyncio
import csv
import re
from playwright.async_api import async_playwright
import os

MAIN_URL = "https://www.klebs.info/abfaelle/"
OUTPUT_FILE = "klebs_final.csv"

# ✅ Acceptă cookies dacă există
async def accept_cookies_if_present(page):
    try:
        await page.wait_for_selector('a._brlbs-btn-accept-all', timeout=5000)
        await page.click('a._brlbs-btn-accept-all')
        print("✅Accepted cookies")
    except:
        print("ℹ️ No pop-up cookies")

# ✅ Obține link-urile din grila de pe pagina principală
async def get_card_links(page):
    await page.goto(MAIN_URL)
    await accept_cookies_if_present(page)
    await page.wait_for_timeout(1500)

    cards = await page.query_selector_all("div.fn-panel > a")
    links = []

    for card in cards:
        href = await card.get_attribute("href")
        if href:
            if href.startswith("/"):
                href = "https://www.klebs.info" + href
            links.append(href)

    print(f"🔗 Waste card links: {len(links)}")
    return links

# ✅ Caută containere pe pagina cardului
async def get_container_links(page, url):
    await page.goto(url)
    await page.mouse.wheel(0, 1000)
    await page.wait_for_timeout(1000)

    elements = await page.query_selector_all('a')
    links = []
    for el in elements:
        href = await el.get_attribute('href')
        if href and "/containerdienst/" in href:
            if href.startswith("/"):
                href = "https://www.klebs.info" + href
            if not href.endswith("/containerdienst/") and not href.endswith("/kleincontainer/"):
                if href not in links:
                    links.append(href)
    print(f"📦 {len(links)} containers found in: {url}")
    return links

# ✅ Extrage prețul din text
def parse_price(text):
    for line in text.splitlines():
        if "Mietpreis" in line or "inkl MwSt" in line:
            match = re.search(r"(\d{1,3}(?:\.\d{3})*,\d{2})", line)
            if match:
                price_str = match.group(1)
                price_clean = price_str.replace(".", "").replace(",", ".")
                try:
                    return f"{price_str} €", float(price_clean), line
                except:
                    return price_str, "", line
    return "", "", ""

# ✅ Deschide pagina unui container și extrage datele
async def extract_page_data(page, url):
    await page.goto(url)
    await page.wait_for_timeout(1000)
    text = await page.inner_text("body")

    produkt = ""
    größe = ""
    
    lines = text.splitlines()
    for line in lines:
        if "cbm" in line.lower() and "container" in line.lower():
            match = re.search(r"(\d{1,2})\s*cbm.*?(container|Container)", line, re.IGNORECASE)
            if match:
                größe = match.group(1)
                produkt = line.strip().lower()
                break

    preis, preis_numerisch, kontext = parse_price(text)

    return [produkt, größe, preis, preis_numerisch, kontext, "", url]

# ✅ Program principal
async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, slow_mo=200)
        page = await browser.new_page()
        all_data = [["produkt", "größe", "preis", "preis_numerisch", "kontext", "fehler", "link"]]

        card_links = await get_card_links(page)

        for sub_url in card_links:
            container_links = await get_container_links(page, sub_url)
            if not container_links:
                continue

            for container_url in container_links:
                try:
                    row = await extract_page_data(page, container_url)
                    all_data.append(row)
                    print(f"[✔] {row}")
                except Exception as e:
                    print(f"[!] Error at: {container_url} -> {e}")
                    all_data.append(["", "", "", "", "", str(e), container_url])

        await browser.close()

        # ✅ Salvează toate datele brute
        with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerows(all_data)

        print(f"\n✅ Final CSV saved: {OUTPUT_FILE}")
        return all_data

# 🔁 Rulează și filtrează după
all_data = asyncio.run(main())

# ✅ Filtrare doar rânduri valide (cu "inkl MwSt" în context)
# ✅ Filtrare doar rânduri valide (cele cu "inkl MwSt" în contextul prețului)
filtered_data = []
for row in all_data:
    if len(row) > 4 and "inkl MwSt" in row[4]:
        filtered_data.append(row)

# ✅ Salvează doar datele filtrate în CSV final
os.makedirs("results_klebs", exist_ok=True)
with open(os.path.join("results_klebs", "klebs_filtered.csv"), 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)  # ✅ DEFINEȘTE writer
    writer.writerow(["produkt", "größe", "preis", "preis_numerisch", "kontext", "fehler", "link"])
    writer.writerows(filtered_data)

print("✅ Saved filtered CSV: klebs_filtered.csv")

# ✅ Șterge fișierul klebs_final.csv după ce a fost procesat
os.remove(OUTPUT_FILE)
print(f"✅ The file {OUTPUT_FILE} has been deleted.")
