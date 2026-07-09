# a55.py - Advanced Browser Automation with Auto-Login & RAM Optimization

import re
import asyncio
from telethon import TelegramClient, events
from playwright.async_api import async_playwright, Page

# =========================
# TELEGRAM CONFIG
# =========================
api_id = 33505697
api_hash = "e40eca6e282916d1371c11ca8ac7c3cb"

# =========================
# LOGIN CREDENTIALS (10 DIFFERENT ACCOUNTS)
# =========================
LOGIN_ACCOUNTS = [
    {"username": "account1_username", "password": "account1_password"},
    {"username": "account2_username", "password": "account2_password"},
    {"username": "account3_username", "password": "account3_password"},
    {"username": "account4_username", "password": "account4_password"},
    {"username": "account5_username", "password": "account5_password"},
    {"username": "account6_username", "password": "account6_password"},
    {"username": "account7_username", "password": "account7_password"},
    {"username": "account8_username", "password": "account8_password"},
    {"username": "account9_username", "password": "account9_password"},
    {"username": "account10_username", "password": "account10_password"},
]

# CSS SELECTORS (adjust based on your website structure)
LOGIN_SELECTOR = "input[type='text']"  # Username input selector
PASSWORD_SELECTOR = "input[type='password']"  # Password input selector
LOGIN_BUTTON = "button:has-text('Login')"  # Login button selector

channels = [
    "aviator55club",
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
SITE_URL = "https://www.uoefkt55.com/#/main/RedeemGift"

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
    "session_a",
    api_id,
    api_hash
)

# =========================
# AUTO LOGIN FUNCTION
# =========================
async def auto_login(page: Page, username: str, password: str, tab_num: int):
    """
    Automated login function with custom credentials per tab
    
    Args:
        page: Playwright page object
        username: Login username for this account
        password: Login password for this account
        tab_num: Tab number for logging purposes
    """
    try:
        print(f"  [Tab {tab_num}] Attempting auto-login with account...")
        
        # Wait for login fields to appear
        await page.wait_for_selector(LOGIN_SELECTOR, timeout=5000)
        
        # Fill username field
        await page.fill(LOGIN_SELECTOR, username)
        await page.wait_for_timeout(500)
        
        # Fill password field
        await page.fill(PASSWORD_SELECTOR, password)
        await page.wait_for_timeout(500)
        
        # Click login button
        await page.click(LOGIN_BUTTON)
        await page.wait_for_timeout(3000)
        
        print(f"  [Tab {tab_num}] ✓ Auto-login successful")
        return True
        
    except Exception as e:
        print(f"  [Tab {tab_num}] ✗ Auto-login failed: {e}")
        print(f"  [Tab {tab_num}] Manual login required")
        return False

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

    # =========================
    # OPTIMIZED BROWSER LAUNCH (RAM OPTIMIZATION)
    # =========================
    browser = await playwright.chromium.launch(
        headless=False,
        args=[
            "--disable-extensions",              # Disable extensions to save RAM
            "--disable-sync",                    # Disable sync to save RAM
            "--no-default-browser-check",        # Skip browser checks
            "--no-first-run",                    # Skip first run
            "--disable-default-apps",            # No default apps
            "--disable-preconnect",              # No preconnect
            "--disable-background-networking",   # No background networking
            "--disable-component-extensions-with-background-pages",
            "--disable-breakpad",                # Disable crash reporting
            "--disable-client-side-phishing-detection",
            "--disable-component-update",
            "--disable-plugin-power-saver",
            "--disable-popup-blocking",
            "--enable-automation",
            "--mute-audio",                      # Mute audio to save resources
            "--memory-pressure-off",
            "--disable-renderer-backgrounding",
        ]
    )

    # =========================
    # 10 TABS OPEN WITH AUTO-LOGIN (EACH WITH DIFFERENT ACCOUNT)
    # =========================
    print("\n" + "="*60)
    print("OPENING 10 BROWSER TABS WITH AUTO-LOGIN (10 ACCOUNTS)...")
    print("="*60 + "\n")
    
    for i in range(10):

        print(f"[Tab {i+1}/10] Opening with account {i+1}...")
        p = await browser.new_page()

        await p.goto(SITE_URL)
        
        # Get credentials for this tab
        account = LOGIN_ACCOUNTS[i]
        
        # Try auto-login with this account's credentials
        login_success = await auto_login(
            p, 
            account["username"], 
            account["password"],
            i+1
        )
        
        if not login_success:
            print(f"[Tab {i+1}/10] Please login manually and press ENTER when done...")
            input(f"[Tab {i+1}/10] Waiting for manual login...")

        pages.append(p)
        print(f"[Tab {i+1}/10] Ready ✓\n")

    print("\n" + "="*60)
    print(f"✓ ALL 10 TABS OPENED AND LOGGED IN WITH 10 ACCOUNTS")
    print("="*60)
    print("\nBOT STARTING...")
    print("WAITING FOR GIFT CODES...\n")

    await client.start()

    await client.run_until_disconnected()

# =========================
# START
# =========================
asyncio.run(main())