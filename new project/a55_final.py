# ============================================================================
# GIFT CODE REDEEMER BOT v3.0 - With Config File Support
# ============================================================================
# Now uses config.json for easy setup - No need to edit Python code!
# ============================================================================

import re
import asyncio
import json
import logging
import os
from typing import List, Dict, Optional, Tuple
from telethon import TelegramClient, events
from playwright.async_api import async_playwright, Browser, Page
from pathlib import Path

# ============================================================================
# CONFIGURATION LOADING
# ============================================================================

CONFIG_FILE = "config.json"

def load_config() -> Dict:
    """Load configuration from JSON file"""
    if not os.path.exists(CONFIG_FILE):
        print("\n" + "="*70)
        print("  ✗ ERROR: config.json not found!")
        print("="*70)
        print("\n  Please run: python setup_wizard.py\n")
        exit(1)
    
    try:
        with open(CONFIG_FILE, 'r') as f:
            config = json.load(f)
        return config
    except json.JSONDecodeError as e:
        print(f"\n  ✗ Error parsing config.json: {e}\n")
        exit(1)
    except Exception as e:
        print(f"\n  ✗ Error loading config.json: {e}\n")
        exit(1)

CONFIG = load_config()

# Extract configuration
TELEGRAM_CONFIG = CONFIG.get("telegram", {})
SITE_CONFIG = CONFIG.get("website", {})
LOGIN_ACCOUNTS = [acc for acc in CONFIG.get("accounts", []) if acc.get("enabled", True)]
TELEGRAM_CHANNELS = CONFIG.get("telegram_channels", [])
TIMEOUTS = CONFIG.get("timeouts", {})
FEATURES = CONFIG.get("features", {})

# ============================================================================
# LOGGING CONFIGURATION
# ============================================================================

log_level = logging.INFO if FEATURES.get("enable_logging", True) else logging.WARNING

logging.basicConfig(
    level=log_level,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ============================================================================
# GLOBAL STATE
# ============================================================================

pages: List[Page] = []
browsers: List[Browser] = []
browser: Optional[Browser] = None  # kept for compatibility
playwright_instance = None
NUM_WINDOWS = 10
client: Optional[TelegramClient] = None
login_stats = {"success": 0, "failed": 0, "manual": 0}
redeem_stats = {"success": 0, "error": 0, "ran_out": 0, "unknown": 0}

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def print_header(text: str) -> None:
    """Print formatted header"""
    print("\n" + "="*70)
    print(f"  {text}")
    print("="*70 + "\n")

def print_success(tab_num: int, message: str) -> None:
    """Print success message"""
    print(f"  [Tab {tab_num:2d}] ✓ {message}")

def print_error(tab_num: int, message: str) -> None:
    """Print error message"""
    print(f"  [Tab {tab_num:2d}] ✗ {message}")

def print_info(tab_num: int, message: str) -> None:
    """Print info message"""
    print(f"  [Tab {tab_num:2d}] ℹ {message}")

def get_timeout(key: str) -> int:
    """Get timeout value from config"""
    return TIMEOUTS.get(key, 5000)

# ============================================================================
# AUTO-LOGIN FUNCTION (WITH RETRY LOGIC)
# ============================================================================

async def auto_login(page: Page, username: str, password: str, tab_num: int, retry: int = 0) -> bool:
    """
    Automated login with retry logic and comprehensive error handling
    
    Args:
        page: Playwright page object
        username: Account username
        password: Account password
        tab_num: Tab number for logging
        retry: Current retry attempt
        
    Returns:
        True if login successful, False otherwise
    """
    max_retries = FEATURES.get("max_retries", 3)
    
    try:
        if retry == 0:
            print_info(tab_num, f"Attempting auto-login...")
        else:
            print_info(tab_num, f"Retry attempt {retry}/{max_retries}...")
        
        # Wait for login selector with timeout
        try:
            await page.wait_for_selector(
                SITE_CONFIG.get("login_selector", "input[type='text']"),
                timeout=get_timeout("selector")
            )
        except Exception as e:
            if retry < max_retries and FEATURES.get("retry_failed_logins", True):
                await page.wait_for_timeout(1000)
                return await auto_login(page, username, password, tab_num, retry + 1)
            else:
                print_error(tab_num, f"Login field not found: {str(e)[:40]}")
                return False
        
        # Clear and fill username field
        await page.fill(SITE_CONFIG.get("login_selector", "input[type='text']"), "")
        await page.wait_for_timeout(get_timeout("input_delay"))
        await page.fill(SITE_CONFIG.get("login_selector", "input[type='text']"), username)
        await page.wait_for_timeout(get_timeout("input_delay"))
        
        # Fill password field
        await page.fill(SITE_CONFIG.get("password_selector", "input[type='password']"), password)
        await page.wait_for_timeout(get_timeout("input_delay"))
        
        # Click login button
        try:
            await page.click(SITE_CONFIG.get("login_button", "button:has-text('Login')"))
        except Exception as e:
            if retry < max_retries and FEATURES.get("retry_failed_logins", True):
                await page.wait_for_timeout(1000)
                return await auto_login(page, username, password, tab_num, retry + 1)
            else:
                print_error(tab_num, f"Login button click failed")
                return False
        
        # Wait for login to complete
        await page.wait_for_timeout(get_timeout("login"))
        
        print_success(tab_num, "Auto-login successful")
        global login_stats
        login_stats["success"] += 1
        return True
        
    except Exception as e:
        if retry < max_retries and FEATURES.get("retry_failed_logins", True):
            await page.wait_for_timeout(1000)
            return await auto_login(page, username, password, tab_num, retry + 1)
        
        print_error(tab_num, f"Auto-login failed: {str(e)[:50]}")
        login_stats["failed"] += 1
        return False

# ============================================================================
# CODE REDEMPTION FUNCTIONS
# ============================================================================

async def close_popup(page: Page) -> None:
    """Close confirmation popup if it exists"""
    try:
        confirm_btn = page.locator(SITE_CONFIG.get("confirm_button", "button:has-text('Confirm')"))
        if await confirm_btn.count() > 0:
            await confirm_btn.click(force=True)
            await page.wait_for_timeout(get_timeout("action"))
    except Exception:
        pass

async def redeem_code_on_page(page: Page, code: str, tab_num: int) -> str:
    """
    Redeem a gift code on a single page
    
    Args:
        page: Playwright page object
        code: Gift code to redeem
        tab_num: Tab number for logging
        
    Returns:
        Result status (success, error, ran_out, unknown)
    """
    try:
        # Close any existing popup
        await close_popup(page)
        
        # Clear previous code
        try:
            await page.fill(SITE_CONFIG.get("code_input", "input[type='text']"), "")
            await page.wait_for_timeout(get_timeout("input_delay"))
        except Exception:
            pass
        
        # Enter new code
        await page.fill(SITE_CONFIG.get("code_input", "input[type='text']"), code)
        await page.wait_for_timeout(get_timeout("input_delay"))
        
        # Click receive button
        try:
            await page.click(SITE_CONFIG.get("receive_button", "button:has-text('Receive')"), force=True)
        except Exception as e:
            print_error(tab_num, f"Receive button click failed")
            return "error"
        
        # Wait for response
        await page.wait_for_timeout(get_timeout("action"))
        
        # Check response
        try:
            content = await page.content()
            
            if "Successfully received" in content:
                print_success(tab_num, f"Code {code[:8]}... redeemed ✓")
                global redeem_stats
                redeem_stats["success"] += 1
                return "success"
            elif "Redemption code error" in content:
                print_info(tab_num, f"Invalid code: {code[:8]}...")
                redeem_stats["error"] += 1
                return "error"
            elif "ran out" in content.lower():
                print_info(tab_num, f"Code {code[:8]}... already used")
                redeem_stats["ran_out"] += 1
                return "ran_out"
            else:
                redeem_stats["unknown"] += 1
                return "unknown"
        except Exception as e:
            print_error(tab_num, f"Response check failed")
            redeem_stats["error"] += 1
            return "error"
            
    except Exception as e:
        print_error(tab_num, f"Redeem failed: {str(e)[:50]}")
        redeem_stats["error"] += 1
        return "error"

async def redeem_code(code: str) -> None:
    """Redeem code on all active pages"""
    if not pages:
        logger.warning(f"No pages available to redeem code: {code}")
        return
    
    print(f"\n{'='*70}")
    print(f"  🎁 NEW CODE FOUND: {code}")
    print(f"  {'='*70}")
    print(f"  Redeeming on {len(pages)} accounts...\n")
    
    tasks = []
    for idx, page in enumerate(pages, 1):
        tasks.append(redeem_code_on_page(page, code, idx))
    
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    # Count results
    success_count = sum(1 for r in results if r == "success")
    error_count = sum(1 for r in results if r == "error")
    ran_out_count = sum(1 for r in results if r == "ran_out")
    
    print(f"\n  Summary: ✓ {success_count} success | ✗ {error_count} errors | ⚠ {ran_out_count} ran out\n")

# ============================================================================
# TELEGRAM FUNCTIONS
# ============================================================================

async def initialize_telegram_client() -> TelegramClient:
    """Initialize and return Telegram client"""
    client = TelegramClient(
        "session_a",
        TELEGRAM_CONFIG.get("api_id"),
        TELEGRAM_CONFIG.get("api_hash")
    )
    return client

async def setup_telegram_handler(client: TelegramClient) -> None:
    """Setup message handler for Telegram"""
    @client.on(events.NewMessage(chats=TELEGRAM_CHANNELS))
    async def handler(event):
        text = event.raw_text
        logger.info(f"New message from {event.chat_id}")
        
        # Extract 32-character hex codes
        codes = re.findall(r'\b[A-Fa-f0-9]{32}\b', text)
        
        if codes:
            for code in codes:
                await redeem_code(code)

# ============================================================================
# BROWSER INITIALIZATION
# ============================================================================

BROWSER_ARGS = [
    "--disable-extensions",
    "--disable-sync",
    "--disable-default-apps",
    "--disable-breakpad",
    "--disable-client-side-phishing-detection",
    "--disable-component-update",
    "--disable-plugin-power-saver",
    "--disable-popup-blocking",
    "--disable-background-networking",
    "--disable-preconnect",
    "--disable-component-extensions-with-background-pages",
    "--mute-audio",
    "--memory-pressure-off",
    "--disable-renderer-backgrounding",
    "--no-default-browser-check",
    "--no-first-run",
    "--enable-automation",
]

async def launch_single_window(tab_num: int) -> Optional[Page]:
    """Launch a completely separate browser window (separate OS process) for one account."""
    global login_stats

    account = LOGIN_ACCOUNTS[(tab_num - 1) % len(LOGIN_ACCOUNTS)] if LOGIN_ACCOUNTS else {}

    try:
        # Each call to chromium.launch() = a NEW separate browser window
        bw = await playwright_instance.chromium.launch(
            headless=FEATURES.get("headless_mode", False),
            args=BROWSER_ARGS,
        )

        page = await bw.new_page()
        page._bw_ref = bw  # attach so cleanup can reach it

        print(f"  [Win {tab_num:2d}] Opening page...")
        try:
            await page.goto(SITE_CONFIG.get("url", ""), timeout=get_timeout("page_load"))
        except Exception as e:
            print_error(tab_num, f"Failed to load page: {str(e)[:50]}")
            await bw.close()
            return None

        if FEATURES.get("auto_login", True) and account:
            login_success = await auto_login(page, account["username"], account["password"], tab_num)
        else:
            login_success = False

        if not login_success:
            print_info(tab_num, "Please login manually in this window...")
            loop = asyncio.get_event_loop()
            try:
                await loop.run_in_executor(
                    None, lambda: input(f"  [Win {tab_num:2d}] Press ENTER after login: ")
                )
                login_stats["manual"] += 1
            except (KeyboardInterrupt, EOFError):
                print_error(tab_num, "Skipped by user")
                await bw.close()
                return None

        browsers.append(bw)
        print_success(tab_num, "Window ready")
        return page

    except Exception as e:
        logger.error(f"Error setting up window {tab_num}: {e}")
        return None

async def initialize_browser() -> None:
    """Playwright is started in main(); this is kept for compatibility."""
    pass

async def setup_pages() -> None:
    """Open NUM_WINDOWS completely separate browser windows in parallel."""
    global pages

    if not LOGIN_ACCOUNTS:
        raise RuntimeError("No accounts configured in config.json!")

    print_header(f"Opening {NUM_WINDOWS} Separate Browser Windows")
    print(f"  Accounts in config : {len(LOGIN_ACCOUNTS)}")
    print(f"  Windows to open    : {NUM_WINDOWS}")
    if len(LOGIN_ACCOUNTS) < NUM_WINDOWS:
        print(f"  ⚠  Fewer accounts than windows — accounts will be cycled\n")

    # asyncio.gather launches all 10 windows at the same time (parallel)
    results = await asyncio.gather(
        *[launch_single_window(i + 1) for i in range(NUM_WINDOWS)],
        return_exceptions=True
    )

    for result in results:
        if isinstance(result, Page):
            pages.append(result)

    if not pages:
        raise RuntimeError("Failed to initialize any browser windows!")

    print_header(f"✓ Ready: {len(pages)}/{NUM_WINDOWS} Windows Active")

# ============================================================================
# CLEANUP FUNCTION
# ============================================================================

async def cleanup() -> None:
    """Cleanup resources gracefully"""
    print_header("Cleaning Up & Saving Stats")
    
    # Close all pages and their browser windows
    closed = set()
    for page in pages:
        try:
            await page.close()
        except Exception:
            pass
        bw = getattr(page, "_bw_ref", None)
        if bw and id(bw) not in closed:
            try:
                await bw.close()
                closed.add(id(bw))
            except Exception as e:
                logger.error(f"Error closing browser: {e}")
    for bw in browsers:
        if id(bw) not in closed:
            try:
                await bw.close()
            except Exception as e:
                logger.error(f"Error closing browser: {e}")
    
    # Stop playwright
    if playwright_instance:
        try:
            await playwright_instance.stop()
        except Exception as e:
            logger.error(f"Error stopping playwright: {e}")
    
    # Disconnect Telegram client
    if client:
        try:
            await client.disconnect()
        except Exception as e:
            logger.error(f"Error disconnecting Telegram: {e}")
    
    # Print statistics
    total_logins = login_stats["success"] + login_stats["failed"] + login_stats["manual"]
    print(f"  Login Stats:")
    print(f"    ✓ Auto-login Success: {login_stats['success']}")
    print(f"    ✗ Auto-login Failed: {login_stats['failed']}")
    print(f"    👤 Manual Login: {login_stats['manual']}")
    
    total_redeems = redeem_stats["success"] + redeem_stats["error"] + redeem_stats["ran_out"] + redeem_stats["unknown"]
    if total_redeems > 0:
        print(f"\n  Redemption Stats:")
        print(f"    ✓ Success: {redeem_stats['success']}")
        print(f"    ✗ Errors: {redeem_stats['error']}")
        print(f"    ⚠ Ran Out: {redeem_stats['ran_out']}")
    
    logger.info("Cleanup completed")

# ============================================================================
# MAIN FUNCTION
# ============================================================================

async def main() -> None:
    """Main application loop"""
    global browser, client, playwright_instance
    
    try:
        print("\n")
        print("╔" + "="*68 + "╗")
        print("║" + " "*18 + "GIFT CODE REDEEMER BOT v3.0" + " "*23 + "║")
        print("║" + " "*8 + "Multi-Account | Auto-Login | 10 Separate Windows | RAM Optimized" + " "*7 + "║")
        print("╚" + "="*68 + "╝")
        
        # Show active configuration
        print(f"\n  Configuration Loaded:")
        print(f"    • Active Accounts : {len(LOGIN_ACCOUNTS)}")
        print(f"    • Browser Windows : {NUM_WINDOWS}")
        print(f"    • Channels        : {len(TELEGRAM_CHANNELS)}")
        print(f"    • Auto-login      : {'Enabled' if FEATURES.get('auto_login', True) else 'Disabled'}")
        print(f"    • Retry Logic     : {'Enabled' if FEATURES.get('retry_failed_logins', True) else 'Disabled'}")
        
        # Start Playwright (one instance drives all 10 separate browsers)
        print_header("Initializing Browser Engine")
        playwright_instance = await async_playwright().start()
        logger.info("Playwright started")
        
        # Open 10 separate browser windows in parallel
        await setup_pages()
        
        # Initialize Telegram
        print_header("Initializing Telegram Client")
        client = await initialize_telegram_client()
        await setup_telegram_handler(client)
        
        print_header("Bot Started - Monitoring Gift Codes")
        print(f"  Watching {len(TELEGRAM_CHANNELS)} Telegram channels for gift codes...")
        print(f"  Redeeming on {len(pages)} active accounts in parallel...\n")
        
        # Start Telegram client
        await client.start()
        logger.info("Telegram client started")
        
        # Keep running until disconnected
        await client.run_until_disconnected()
        
    except KeyboardInterrupt:
        print("\n\n  ⚠ Bot interrupted by user")
    except Exception as e:
        logger.error(f"Fatal error in main: {e}", exc_info=True)
        print(f"\n  ✗ Fatal error: {e}")
    finally:
        await cleanup()
        print("\n  Bot shutdown complete.\n")

# ============================================================================
# ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n  Program terminated by user")
    except Exception as e:
        logger.error(f"Unhandled exception: {e}", exc_info=True)
