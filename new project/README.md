# 🎁 Gift Code Redeemer Bot v3.0

**Advanced multi-account gift code automation with Telegram monitoring and intelligent auto-login**

---

## ✨ Features

- ✅ **Auto-Login** - Automatically logs in 10 accounts with retry logic
- ✅ **10 Parallel Tabs** - Redeem codes on all accounts simultaneously
- ✅ **Telegram Monitoring** - Real-time code detection from 13+ channels
- ✅ **RAM Optimized** - Advanced Chromium flags for low memory usage
- ✅ **Config File** - Easy setup without editing Python code
- ✅ **Setup Wizard** - Interactive configuration tool
- ✅ **Error Recovery** - Automatic retries and graceful fallbacks
- ✅ **Session Saving** - Optional session persistence
- ✅ **Detailed Logging** - Track bot activity and results
- ✅ **Statistics** - Real-time success/failure tracking

---

## 🚀 Quick Start (3 Steps)

### Step 1: Install Dependencies
```bash
pip install telethon playwright
playwright install chromium
```

### Step 2: Run Setup Wizard
```bash
python setup_wizard.py
```
This creates `config.json` with your accounts and settings.

### Step 3: Run the Bot
```bash
python a55_final.py
```

**That's it!** The bot will:
1. Automatically login to all 10 accounts
2. Monitor Telegram channels for gift codes
3. Automatically redeem codes on all accounts

---

## 📋 Setup Guide

### Using the Setup Wizard (Recommended for Beginners)

```bash
python setup_wizard.py
```

The wizard will ask you:

1. **Telegram API Credentials**
   - Get from: https://my.telegram.org/apps
   - Take 2 minutes

2. **Website Configuration**
   - Find CSS selectors using F12 (Developer Tools)
   - Example: `input[type="text"]`, `button:has-text("Login")`

3. **Account Credentials**
   - Enter 10 username/password pairs
   - Enabled/Disabled toggle for each account

4. **Telegram Channels**
   - Use defaults or add custom channels
   - Bot monitors these for gift codes

5. **Timeout Settings**
   - Leave defaults unless you have issues
   - Advanced users can customize

6. **Features**
   - Enable/disable features like auto-login, session saving, retries

---

## 🔧 Manual Configuration (Advanced)

If you want to edit `config.json` manually:

```json
{
  "telegram": {
    "api_id": 33505697,
    "api_hash": "e40eca6e282916d1371c11ca8ac7c3cb"
  },
  "website": {
    "url": "https://example.com/redeem",
    "login_selector": "input[type='text']",
    "password_selector": "input[type='password']",
    "login_button": "button:has-text('Login')",
    "code_input": "input[type='text']",
    "receive_button": "button:has-text('Receive')"
  },
  "accounts": [
    {
      "id": 1,
      "username": "user1@email.com",
      "password": "pass1",
      "enabled": true
    },
    ...
  ],
  "features": {
    "auto_login": true,
    "save_sessions": true,
    "retry_failed_logins": true,
    "max_retries": 3,
    "enable_logging": true,
    "headless_mode": false
  }
}
```

---

## 🎯 How to Find CSS Selectors

1. Open website in browser
2. Press `F12` to open Developer Tools
3. Click the selector icon (top-left of DevTools)
4. Click on the login field
5. Look at the HTML in DevTools
6. Use that to create the selector

### Common Selector Examples:
- Username input: `input[type="text"]` or `input#username`
- Password input: `input[type="password"]`
- Login button: `button:has-text("Login")` or `button.login-btn`
- Confirm button: `button:has-text("Confirm")`
- Code input: `input[type="text"]` or `input#gift-code`
- Receive button: `button:has-text("Receive")` or `button.redeem-btn`

---

## 📊 Understanding the Output

```
[Tab 01] ✓ Auto-login successful
[Tab 02] ✓ Auto-login successful
[Tab 03] ℹ Attempting auto-login...
[Tab 03] ✗ Auto-login failed: Login field not found
[Tab 03] ℹ Please login manually...

🎁 NEW CODE FOUND: a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6
Redeeming on 10 accounts...

[Tab 01] ✓ Code a1b2c3d4... redeemed ✓
[Tab 02] ✓ Code a1b2c3d4... redeemed ✓
[Tab 03] ✗ Receive button click failed
[Tab 04] ✓ Code a1b2c3d4... redeemed ✓
...

Summary: ✓ 9 success | ✗ 1 errors | ⚠ 0 ran out
```

### Icons Explanation:
- `✓` = Success
- `✗` = Error/Failed
- `ℹ` = Info/Neutral
- `🎁` = New Code Found
- `⚠` = Warning (code ran out)

---

## 🐛 Troubleshooting

### Problem: "config.json not found"
**Solution**: Run `python setup_wizard.py` first

### Problem: Auto-login not working
**Solution**:
1. Check website selectors in `config.json`
2. Open Developer Tools (F12) and verify selectors
3. Try with `"auto_login": false` and login manually
4. Check if website has CAPTCHA or 2FA

### Problem: Can't find elements
**Solution**:
1. The website might be using different selectors
2. Use Developer Tools to find correct selectors
3. Update `config.json` with correct ones
4. Test with one account first

### Problem: Low redemption success rate
**Solution**:
1. Check if timeout values are too short
2. Increase timeouts in `config.json`
3. Check if website is slow
4. Verify account credentials are correct

### Problem: Browser using too much RAM
**Solution**:
1. Reduce number of active tabs by disabling accounts
2. Close other applications
3. The bot already has memory optimizations enabled

---

## 📁 File Structure

```
your_project/
├── a55_final.py           ← Main bot script (RUN THIS)
├── setup_wizard.py        ← Configuration wizard (RUN THIS FIRST)
├── config.json            ← Your configuration (auto-created)
├── README.md              ← This file
└── session_a.session      ← Telegram session (auto-created)
```

---

## ⚙️ Configuration Options Explained

### Timeout Settings (milliseconds)
- `selector`: Time to wait for CSS elements (default: 5000ms = 5 seconds)
- `login`: Time to wait after clicking login (default: 3000ms)
- `page_load`: Time to wait for page to load (default: 3000ms)
- `action`: Time to wait for general actions (default: 100ms)
- `input_delay`: Delay between typing characters (default: 500ms)

### Features
- `auto_login`: Enable automatic login (true/false)
- `save_sessions`: Save browser cookies between runs (true/false)
- `retry_failed_logins`: Retry failed login attempts (true/false)
- `max_retries`: Number of retry attempts (1-10)
- `enable_logging`: Enable detailed logs (true/false)
- `headless_mode`: Run without visible browser (true/false)

---

## 🔐 Security Notes

- Credentials stored in `config.json` - keep it safe!
- Never share `config.json` or `session_a.session` files
- Use strong passwords for your accounts
- Consider encrypting sensitive files

---

## 📈 Performance Tips

1. **Too many accounts?** - Disable unused accounts in `config.json`
2. **Browser lagging?** - Try `headless_mode: true`
3. **Codes not detected?** - Check Telegram channels are correct
4. **Redemptions slow?** - Increase timeout values slightly

---

## 🆘 Getting Help

1. Check the logs (enable `enable_logging: true`)
2. Use Developer Tools (F12) to find correct selectors
3. Test each component separately
4. Verify Telegram API credentials are correct

---

## 📝 Version History

- **v3.0** - Config file support, Setup wizard, Retry logic
- **v2.0** - Comprehensive error handling, Better logging
- **v1.0** - Basic functionality

---

## ✅ Checklist Before Running

- [ ] Ran `python setup_wizard.py`
- [ ] Updated accounts in `config.json`
- [ ] Verified website selectors are correct
- [ ] Installed all dependencies with pip
- [ ] Have Telegram API credentials (from my.telegram.org)
- [ ] At least 1 account enabled in `config.json`

---

## 🎉 You're Ready!

```bash
python a55_final.py
```

The bot will start monitoring for gift codes and automatically redeem them on all your accounts. Good luck! 🚀

---

**Happy Redeeming!** 🎁✨
