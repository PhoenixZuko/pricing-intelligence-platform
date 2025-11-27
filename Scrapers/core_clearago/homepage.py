from playwright.async_api import async_playwright

async def launch_browser_and_submit_postcode(postcode, headless=True, pause_on_end=False, return_page=False):
    playwright = await async_playwright().start()
    browser = await playwright.chromium.launch(headless=headless)
    context = await browser.new_context()
    page = await context.new_page()

    print("[→] Navigating to https://www.clearago.de/")
    await page.goto("https://www.clearago.de/", timeout=60000)
    await page.wait_for_load_state("domcontentloaded")
    print("[✓] Page loaded")

    # NEW: Click "Allow all" on Cookiebot if visible
    try:
        await page.wait_for_selector('#CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll', timeout=9000)
        await page.click('#CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll')
        print("[✓] Cookiebot 'Allow all' clicked")
    except:
        print("[i] Cookiebot 'Allow all' not present or already handled")

    # OLD fallback cookie button
    try:
        await page.click('button#cookie-consent-accept-all', timeout=8000)
        print("[✓] Cookie popup accepted")
    except:
        print("[i] No alternate cookie popup")

    # Fill in postcode
    try:
        await page.fill('input[data-test="plz-input-header"]', postcode)
        print(f"[→] Postcode entered: {postcode}")
        await page.click('button[data-test="plz-button-header"]')
        print("[✓] Submit button clicked")
    except Exception as e:
        print(f"[!] Error submitting postcode: {e}")

    await page.wait_for_load_state("networkidle")
    print("[⏳] Waiting for page to fully load...")

    if return_page:
        return page  # Keep browser open for further actions

    if pause_on_end:
        input("[⏸] Press Enter to close the browser...")

    await browser.close()
    await playwright.stop()
