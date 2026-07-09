#!/usr/bin/env python3
# ============================================================================
# SETUP WIZARD - Interactive Configuration Tool
# ============================================================================
# Run this FIRST to configure your bot easily without editing code!
# ============================================================================

import json
import os
from pathlib import Path

CONFIG_FILE = "config.json"

def print_header(text: str):
    """Print formatted header"""
    print("\n" + "="*70)
    print(f"  {text}")
    print("="*70 + "\n")

def print_section(text: str):
    """Print section header"""
    print(f"\n► {text}\n")

def validate_input(prompt: str, required: bool = True) -> str:
    """Get and validate user input"""
    while True:
        value = input(prompt).strip()
        if not value and required:
            print("  ✗ This field is required. Please try again.")
            continue
        return value

def load_config():
    """Load existing config or return default"""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"  ⚠ Error loading config: {e}")
    return None

def save_config(config: dict):
    """Save config to JSON file"""
    try:
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=2)
        print(f"\n  ✓ Config saved to {CONFIG_FILE}")
        return True
    except Exception as e:
        print(f"  ✗ Error saving config: {e}")
        return False

def setup_wizard():
    """Interactive setup wizard"""
    
    print("\n")
    print("╔" + "="*68 + "╗")
    print("║" + " "*20 + "GIFT CODE BOT - SETUP WIZARD" + " "*21 + "║")
    print("║" + " "*15 + "Configure your bot easily without editing code" + " "*8 + "║")
    print("╚" + "="*68 + "╝")
    
    # Load existing config
    existing_config = load_config()
    use_existing = False
    
    if existing_config:
        print_section("Existing Configuration Found")
        response = input("  Would you like to use existing config.json? (y/n): ").lower()
        if response == 'y':
            use_existing = True
            config = existing_config
    
    if not use_existing:
        config = {
            "telegram": {},
            "website": {},
            "accounts": [],
            "telegram_channels": [],
            "timeouts": {},
            "features": {}
        }
        
        # ==================== TELEGRAM SETUP ====================
        print_header("1. Telegram API Configuration")
        print("  Get these from: https://my.telegram.org/apps")
        
        config["telegram"]["api_id"] = int(validate_input("  Enter Telegram API ID: "))
        config["telegram"]["api_hash"] = validate_input("  Enter Telegram API Hash: ")
        print("  ✓ Telegram configured\n")
        
        # ==================== WEBSITE SETUP ====================
        print_header("2. Website Selectors Configuration")
        print("  These are CSS selectors from your website's HTML")
        print("  If unsure, inspect the website with F12 (Developer Tools)")
        
        print_section("Enter CSS Selectors")
        config["website"]["url"] = validate_input("  Website URL: ")
        config["website"]["login_selector"] = validate_input("  Username input selector (e.g., 'input[type=\"text\"]'): ")
        config["website"]["password_selector"] = validate_input("  Password input selector (e.g., 'input[type=\"password\"]'): ")
        config["website"]["login_button"] = validate_input("  Login button selector (e.g., 'button:has-text(\"Login\")'): ")
        config["website"]["confirm_button"] = validate_input("  Confirm button selector (optional): ", required=False) or "button:has-text('Confirm')"
        config["website"]["code_input"] = validate_input("  Code input selector (e.g., 'input[type=\"text\"]'): ")
        config["website"]["receive_button"] = validate_input("  Receive/Redeem button selector (e.g., 'button:has-text(\"Receive\")'): ")
        print("  ✓ Website configured\n")
        
        # ==================== ACCOUNTS SETUP ====================
        print_header("3. Add Your 10 Accounts")
        
        for i in range(10):
            print_section(f"Account {i+1}/10")
            
            account = {
                "id": i + 1,
                "username": validate_input(f"  Account {i+1} Username: "),
                "password": validate_input(f"  Account {i+1} Password: "),
                "enabled": True
            }
            config["accounts"].append(account)
        
        print("  ✓ All 10 accounts configured\n")
        
        # ==================== TELEGRAM CHANNELS ====================
        print_header("4. Telegram Channels (Optional)")
        print("  Press Enter to skip using defaults")
        
        use_defaults = input("  Use default channels? (y/n): ").lower() == 'y'
        
        if use_defaults:
            config["telegram_channels"] = [
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
        else:
            print("  Enter channel names (one per line, type 'DONE' when finished):")
            channels = []
            while True:
                channel = input(f"    Channel {len(channels)+1}: ").strip()
                if channel.upper() == 'DONE':
                    break
                if channel:
                    channels.append(channel)
            config["telegram_channels"] = channels if channels else ["aviator55club"]
        
        print("  ✓ Channels configured\n")
        
        # ==================== TIMEOUTS ====================
        print_header("5. Timeout Settings (Advanced)")
        print("  Leave blank to use defaults (recommended for beginners)")
        
        defaults = {
            "selector": 5000,
            "login": 3000,
            "page_load": 3000,
            "action": 100,
            "input_delay": 500
        }
        
        for key, default in defaults.items():
            value = validate_input(f"  {key} timeout (default {default}ms): ", required=False)
            config["timeouts"][key] = int(value) if value else default
        
        print("  ✓ Timeouts configured\n")
        
        # ==================== FEATURES ====================
        print_header("6. Bot Features")
        
        config["features"]["auto_login"] = input("  Enable auto-login? (y/n): ").lower() == 'y'
        config["features"]["save_sessions"] = input("  Save login sessions? (y/n): ").lower() == 'y'
        config["features"]["retry_failed_logins"] = input("  Retry failed logins? (y/n): ").lower() == 'y'
        config["features"]["max_retries"] = int(validate_input("  Max retry attempts (default 3): ", required=False) or "3")
        config["features"]["enable_logging"] = input("  Enable detailed logging? (y/n): ").lower() == 'y'
        config["features"]["headless_mode"] = input("  Run in headless mode? (y/n, recommended: n): ").lower() == 'y'
        
        print("  ✓ Features configured\n")
    
    # ==================== SAVE CONFIG ====================
    print_header("Configuration Summary")
    
    print(f"  Telegram API ID: {config['telegram']['api_id']}")
    print(f"  Website URL: {config['website']['url']}")
    print(f"  Total Accounts: {len(config['accounts'])}")
    print(f"  Total Channels: {len(config['telegram_channels'])}")
    print(f"  Auto-login: {'Enabled' if config['features']['auto_login'] else 'Disabled'}")
    print(f"  Save Sessions: {'Enabled' if config['features']['save_sessions'] else 'Disabled'}")
    
    if input("\n  Save this configuration? (y/n): ").lower() == 'y':
        if save_config(config):
            print("\n" + "="*70)
            print("  ✓ SETUP COMPLETE!")
            print("="*70)
            print("\n  You can now run: python a55_final.py\n")
            return True
    
    return False

if __name__ == "__main__":
    try:
        setup_wizard()
    except KeyboardInterrupt:
        print("\n\n  Setup cancelled by user.")
    except Exception as e:
        print(f"\n  ✗ Error: {e}")
