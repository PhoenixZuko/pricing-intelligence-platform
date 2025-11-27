from playwright.async_api import async_playwright
import asyncio
import os
import csv
from datetime import datetime

PLZ = "10117"
PUBLIC_PLACE_VALUE = 1

SAVE_FOLDER = "results_ensorgo"

async def run_scraper():
    results = []

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    os.makedirs(SAVE_FOLDER, exist_ok=True)
    filename = os.path.join(SAVE_FOLDER, f"entsorgo_{timestamp}.csv")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, slow_mo=100)
        context = await browser.new_context()
        page = await context.new_page()

        await page.goto("https://app.entsorgo.de/rechner/container", timeout=60000)

        try:
            await page.wait_for_selector("#CybotCookiebotDialog", timeout=5000)
            decline = await page.query_selector("#CybotCookiebotDialogBodyButtonDecline")
            if decline:
                await decline.click()
        except:
            pass

        await page.wait_for_selector("input[name='zipcode'], input[placeholder*='Postleitzahl']")
        await page.fill("input[name='zipcode'], input[placeholder*='Postleitzahl']", PLZ)
        await page.keyboard.press("Tab")
        await asyncio.sleep(1)

        public_option = await page.query_selector(f"div.menu > div.item[data-value='{PUBLIC_PLACE_VALUE}']")
        if public_option and await public_option.is_visible():
            await public_option.click()
        await asyncio.sleep(1)

        weiter_btn = await page.query_selector("a#next-btn") or await page.query_selector("button")
        if weiter_btn:
            await weiter_btn.click()
        await asyncio.sleep(2)

        processed_slugs = set()

        with open(filename, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["produkt", "größe", "preis", "preis_numerisch", "kontext", "fehler"])
            writer.writeheader()

            while True:
                await page.wait_for_selector("div.container-box", timeout=10000)
                container_boxes = await page.query_selector_all("div.container-box")
                box_data = []

                for box in container_boxes:
                    try:
                        slug = await box.get_attribute("data-slug")
                        title = await box.get_attribute("data-title")
                        if slug and slug not in processed_slugs:
                            box_data.append((slug, title))
                    except:
                        continue

                if not box_data:
                    print("\n✅ Toate containerele au fost procesate.")
                    break

                for slug, title in box_data:
                    processed_slugs.add(slug)
                    print(f"\n📦 Container: {title}")

                    try:
                        await page.wait_for_selector(f"div.container-box[data-slug='{slug}'] div.action", timeout=10000)
                        action = await page.query_selector(f"div.container-box[data-slug='{slug}'] div.action")
                        if not action:
                            print(f"⚠️ Nu s-a găsit butonul pentru {title}")
                            continue

                        await action.click()
                        await page.wait_for_selector("div.container-size-list", timeout=10000)
                        await asyncio.sleep(1)

                        try:
                            mehr = await page.query_selector("div.more-container")
                            if mehr:
                                await mehr.click()
                        except:
                            pass

                        items = await page.query_selector_all("div.container-size-list div.item-box:not(.more-container)")

                        for item in items:
                            try:
                                await item.click()
                                await asyncio.sleep(1)

                                name_el = await page.query_selector("div.product__details h3")
                                price_el = await page.query_selector("label#price")

                                name = (await name_el.text_content()).strip() if name_el else "unbekannt"
                                price_text = (await price_el.text_content()).strip() if price_el else "0 €"
                                price_num = float(price_text.replace('€', '').replace('.', '').replace(',', '.'))
                                size = await item.get_attribute("data-size")

                                row = {
                                    "produkt": f"{title} Container",
                                    "größe": size,
                                    "preis": price_text,
                                    "preis_numerisch": price_num,
                                    "kontext": price_text,
                                    "fehler": ""
                                }

                                writer.writerow(row)
                                f.flush()  # ⏱ Salvează în timp real
                                print(f"✅ {title} Container | {size} | {price_text}")

                            except Exception as e:
                                print(f"❌ Eroare item-box: {e}")

                        await page.goto("https://app.entsorgo.de/rechner/container/materials")
                        await asyncio.sleep(2)

                    except Exception as e:
                        print(f"❌ Eroare container {title}: {e}")

        await browser.close()
        return results
