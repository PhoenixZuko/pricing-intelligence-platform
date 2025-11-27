import os
from playwright.async_api import Page

# 🔁 FUNCȚIE PRINCIPALĂ pentru a apela subcategoriile
async def scrape_category_details(page: Page, category_url: str, results_folder: str):
    print(f"[📥] Scraping category page: {category_url}")

    # 👉 Apelăm funcția care parcurge subcategoriile și salvează textul
    await browse_subcategories_and_save_text(page, category_url, results_folder)

# 🔍 FUNCȚIE pentru a parcurge subcategoriile și a salva conținutul
import os
from playwright.async_api import Page

async def browse_subcategories_and_save_text(page: Page, category_url: str, results_folder: str):
    print(f"[📂] Searching subcategories in: {category_url}")

    try:
        await page.wait_for_selector('button[data-test="sub-waste-type-card-button"]', timeout=8000)
        buttons = await page.query_selector_all('button[data-test="sub-waste-type-card-button"]')
    except:
        print("[⚠️] No subcategories found.")
        return

    print(f"[📄] Found {len(buttons)} subcategories.")

    for i, button in enumerate(buttons):
        href = await button.get_attribute("onclick")
        if not href or "window.location.href" not in href:
            print(f"[❌] Could not extract subcategory URL from button {i+1}")
            continue

        sub_url_path = href.split("'")[1]
        sub_url = f"https://www.clearago.de{sub_url_path}"

        new_page = await page.context.new_page()
        print(f"[➡️] Opening subcategory: {sub_url}")
        await new_page.goto(sub_url)

        # Încearcă să găsești și să apeși butonul 'Mehr...' în maxim 3 secunde
        try:
            mehr_button = await new_page.wait_for_selector('div[data-test="rolling-container-more"]', timeout=3000)
            await mehr_button.click()
            print("[🟢] Clicked 'Mehr...' button to expand.")
            await new_page.wait_for_timeout(1000)  # așteaptă puțin după click
        except:
            print("[⚠️] 'Mehr...' button not found or not clickable. Continuing.")
        

        # Salvează tot conținutul text
        try:
            body_text = await new_page.inner_text('body')
        except:
            body_text = "[❌] Failed to read page content."

        url_part = sub_url.replace("https://www.clearago.de/", "").replace("/", "-").strip("-")
        filename = os.path.join(results_folder, f"{url_part}.txt")
        os.makedirs(results_folder, exist_ok=True)

        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"[URL]: {sub_url}\n\n")
            f.write(body_text)

        print(f"[💾] Saved content to {filename}")
        await new_page.close()

