# p55.py

import re
import asyncio
from telethon import TelegramClient, events
from playwright.async_api import async_playwright

# =========================
# TELEGRAM CONFIG
# =========================
api_id = 33505697
api_hash = "e40eca6e282916d1371c11ca8ac7c3cb"

channels = [
    "Gift_code_91club_official",
    "sanzi91clubvip",
    "VIP91_55Hub",
    "MoneyLuteraOfficial",
    "KishanTricks",
    "TrendingCodess",
    "Official_91CLUB_Game",
    "earning_boy123",
    "Okwin_91Club_Codes",
    "yw8js999",
    "club91lite",
    "EarningsGrow"
]

# =========================
# WEBSITE
# =========================
SITE_URL = "https://jaipur91.com/#/main/RedeemGift"

# =========================
# GLOBAL PAGES
# =========================
pages = []

# =========================
# REDEEM FUNCTION
# =========================
async def redeem_code(code):

    global pages

    print(f"\nFOUND CODE : {code}")

    tasks = []

    for page in pages:
        tasks.append(process_page(page, code))

    await asyncio.gather(*tasks)


async def process_page(page, code):

    try:

        # popup close if exists
        # popup close force
        try:

            confirm_btn = page.locator(
                'button:has-text("Confirm")'
            )

            if await confirm_btn.count() > 0:

                await confirm_btn.click(force=True)

                print("POPUP CLOSED")

        except:
            pass

        # old text remove
        await page.fill('input', '')

        # new code paste
        await page.fill('input', code)

        # click receive
        await page.locator(
            'button:has-text("Receive")'
        ).click(force=True)

        await page.wait_for_timeout(100)

        content = await page.content()

        if "Successfully received" in content:
            print("ACTUAL CLAIM SUCCESS")

        elif "Redemption code error" in content:
            print("CODE ERROR")

        elif "ran out" in content.lower():
            print("RAN OUT")

        else:
            print("UNKNOWN RESPONSE")

    except Exception as e:

       print("ERROR :", e)

# =========================
# TELEGRAM CLIENT
# =========================
client = TelegramClient(
    "giftsession_a",
    api_id,
    api_hash
)

# =========================
# MESSAGE HANDLER
# =========================
@client.on(events.NewMessage(chats=channels))
async def handler(event):

    text = event.raw_text

    print("\nNEW MESSAGE:\n")
    print(text)

    # 32-char code detect
    codes = re.findall(
        r'\b[A-Fa-f0-9]{32}\b',
        text
    )

    if codes:

        for code in codes:

            await redeem_code(code)

# =========================
# MAIN
# =========================
async def main():

    global pages

    playwright = await async_playwright().start()

    browser = await playwright.chromium.launch(
        headless=False
    )

    # =========================
    # 5 TABS OPEN
    # =========================
    for i in range(5):

        p = await browser.new_page()

        await p.goto(SITE_URL)

        pages.append(p)

    print("\n5 TABS OPENED...")
    print("LOGIN MANUALLY IN ALL TABS...")

    input("\nAfter all login press ENTER...")

    print("\nBOT STARTED...")
    print("WAITING FOR GIFT CODES...\n")

    await client.start()

    await client.run_until_disconnected()

# =========================
# START
# =========================
asyncio.run(main())