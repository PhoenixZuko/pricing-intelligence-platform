import asyncio
from datetime import datetime
import csv
import os
import re
from playwright.async_api import async_playwright

async def extract_products_from_page(page, data):
    await page.wait_for_selector('div.products', timeout=10000)
    products = await page.query_selector_all('div.product-item')

    for product in products:
        title_el = await product.query_selector('a.title-item')
        price_el = await product.query_selector('span.price')

        title = (await title_el.text_content()).strip() if title_el else "unknown"
        price = (await price_el.text_content()).strip() if price_el else "unknown"

        price_match = re.search(r'(\d{1,3}[\.\d{3}]*,\d{2})', price)
        price_clean = price_match.group(1) if price_match else "unknown"
        price_float = float(price_clean.replace('.', '').replace(',', '.')) if price_match else None

        product_match = re.search(r'^(.*)\s+(\d+)\s*(m³|cbm)', title)
        name = product_match.group(1) if product_match else "unknown"
        size = product_match.group(2) if product_match else "unknown"

        entry = {
            "produkt": name,
            "größe": size,
            "preis": price_clean + " €" if price_clean != "unknown" else "unknown",
            "preis_numerisch": price_float,
            "kontext": title,
            "fehler": None
        }
        data.append(entry)

        # ✅ Display what is saved
        print(f"[SAVED] Product: {name} | Size: {size} | Price: {price_clean} € | Title: {title}")


async def process_category(context, url, data):
    try:
        page = await context.new_page()
        await page.goto(url)
        await page.wait_for_timeout(1000)

        # Dacă există produse, le extragem
        if await page.query_selector('.product-item'):
            await extract_products_from_page(page, data)
        else:
            # Dacă nu există produse, verificăm subcategoriile
            subcats = await page.query_selector_all('div.product-category a')
            for sub in subcats:
                href = await sub.get_attribute('href')
                if href:
                    await process_category(context, href, data)

        await page.close()

    except Exception as e:
        data.append({
            "produkt": "unbekannt",
            "größe": "unbekannt",
            "preis": "unbekannt",
            "preis_numerisch": None,
            "kontext": url,
            "fehler": f"Kategorie-Fehler: {str(e)}"
        })

async def scrape_site():
    data = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, args=["--no-sandbox"])
        context = await browser.new_context()
        page = await context.new_page()

        await page.goto('https://cdz-berlin.de/shop')
        await page.wait_for_selector('div.products')

        category_links = await page.query_selector_all('div.products a')
        visited = set()
        hrefs = []
        for link in category_links:
            href = await link.get_attribute('href')
            if href and href not in visited:
                hrefs.append(href)
                visited.add(href)

        for href in hrefs:
            await process_category(context, href, data)

        await browser.close()


    output_dir = "results_cdz-berlin"
    os.makedirs(output_dir, exist_ok=True)

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = os.path.join(output_dir, f'cdz_container_prices_{timestamp}.csv')
    with open(filename, mode='w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ["produkt", "größe", "preis", "preis_numerisch", "kontext", "fehler"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)

    print(f"Full scraping. File saved in: {filename}")

if __name__ == "__main__":
    asyncio.run(scrape_site())
