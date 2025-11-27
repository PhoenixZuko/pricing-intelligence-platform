# core_clearago/waste_categories.py
from playwright.async_api import Page
from core_clearago.details_scraper import scrape_category_details
import os

async def browse_waste_categories(page: Page, results_folder: str):
    print("[2] Browsing waste categories...")

    # Wait for cards to appear
    await page.wait_for_selector('div[data-test="waste-type-card"]', timeout=60000)
    cards = await page.query_selector_all('div[data-test="waste-type-card"]')

    print(f"[📦] Found {len(cards)} waste categories")

    for i, card in enumerate(cards):
        title = await card.query_selector('h3')
        title_text = (await title.inner_text()).strip() if title else f"category_{i+1}"

        button = await card.query_selector('button[data-test="waste-type-card-button"]')
        if not button:
            print(f"[❌] No button found for {title_text}")
            continue

        # Open in new tab (sa nu pierdem sesiunea curentă)
        href = await button.get_attribute("onclick")
        if href and "window.location.href" in href:
            url_path = href.split("'")[1]
            full_url = f"https://www.clearago.de{url_path}"

            print(f"[➡️] Navigating to: {full_url}")
            new_page = await page.context.new_page()
            await new_page.goto(full_url)

            # Scrape & save
            await scrape_category_details(new_page, full_url, results_folder)

            await new_page.close()
        else:
            print(f"[⚠️] Could not parse button URL for {title_text}")
