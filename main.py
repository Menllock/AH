import time
import subprocess
import pyautogui
import keyboard
import sys
from datetime import datetime

# ============ CONFIGURATION VARIABLES ============
# Timing
STARTUP_DELAY = 10          # Wait after launching WoW
LOGIN_DELAY = 20            # Wait after pressing enter on login
CHAR_SELECT_DELAY = 20      # Wait after character selection
MAIL_WAIT = 20              # Wait at mail
RESTOCK_WAIT = 10           # Wait after restock
SCAN_WAIT = 60              # Wait for scan (1 minute)
SHOP_WAIT = 30              # Wait for shop search
RL_WAIT = 10                # Wait after /rl
CREATE_SCAN_WAIT = 30       # Wait after create scan

# Click timing
CLICK_DURATION = 0.05       # How long to hold click (seconds)
CLICK_BREAK = 0.05          # Break between clicks (seconds)
CLICKS_50_COUNT = 50        # Number of clicks for 50-click actions

# Login credentials
USERNAME = "anubera"
PASSWORD = "anubera"

# Coordinates (fill these in!)
COORD_CHARSELECT = (0, 0)      # Character selection screen click
COORD_MAIL = (0, 0)            # Mailbox position
COORD_MAILALL = (0, 0)         # Take all mail button
COORD_NPCBANNER = (0, 0)       # NPC/banner position
COORD_RESTOCK = (0, 0)         # Restock button
COORD_SCANCANCEL = (0, 0)      # Cancel scan button
COORD_CANCEL = (0, 0)          # Cancel confirmation button
COORD_TABSHOP = (0, 0)         # Shop tab
COORD_SHOPSEARCH = (0, 0)      # Shop search field
COORD_SEARCHTOPITEM = (0, 0)   # Top search result item
COORD_SHOPBUY = (0, 0)         # Buy button in shop
COORD_CREATESCAN = (0, 0)      # Create scan button
COORD_CREATEPOST = (0, 0)      # Create post button

# WoW executable path (update this!)
WOW_EXE_PATH = r"C:\Program Files (x86)\World of Warcraft\_retail_\Wow.exe"

# ============ HELPER FUNCTIONS ============

def log_message(message):
    """Print message with timestamp"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] {message}")

def safe_click(coords, description="", delay_before=0.1):
    """Safely click at coordinates with small random delay"""
    if delay_before > 0:
        time.sleep(delay_before)
    
    # Add tiny randomness to avoid detection
    x, y = coords
    if x == 0 and y == 0:
        log_message(f"WARNING: {description} coordinates not set! (0,0)")
        return
    
    rand_x = x + pyautogui.random.randint(-2, 2)
    rand_y = y + pyautogui.random.randint(-2, 2)
    
    pyautogui.moveTo(rand_x, rand_y, duration=0.1)
    pyautogui.click()
    log_message(f"Clicked at {description}: ({rand_x}, {rand_y})")

def multi_click(coords, count, description="", click_duration=CLICK_DURATION, break_duration=CLICK_BREAK):
    """Perform multiple clicks with hold and release pattern"""
    x, y = coords
    if x == 0 and y == 0:
        log_message(f"WARNING: {description} coordinates not set! (0,0)")
        return
    
    rand_x = x + pyautogui.random.randint(-2, 2)
    rand_y = y + pyautogui.random.randint(-2, 2)
    pyautogui.moveTo(rand_x, rand_y, duration=0.1)
    
    for i in range(count):
        pyautogui.mouseDown()
        time.sleep(click_duration)
        pyautogui.mouseUp()
        log_message(f"  Click {i+1}/{count} at {description}")
        if i < count - 1:  # Don't sleep after last click
            time.sleep(break_duration)

def press_key_with_delay(key, delay_before=0.1):
    """Press a key with small delay"""
    time.sleep(delay_before)
    pyautogui.press(key)
    log_message(f"Pressed key: {key}")

def type_string_with_delay(text, delay_before=0.1):
    """Type a string with delay"""
    time.sleep(delay_before)
    pyautogui.write(text)
    log_message(f"Typed: {text}")

# ============ MAIN SCRIPT ============

def main():
    log_message("Starting WoW Disenchanting Bot...")
    log_message("Press F6 to emergency stop")
    
    # Emergency stop listener
    emergency_stop = False
    def stop_script():
        nonlocal emergency_stop
        emergency_stop = True
        log_message("EMERGENCY STOP ACTIVATED!")
    
    keyboard.add_hotkey('f6', stop_script)
    
    try:
        # Step 1: Launch WoW
        log_message(f"Launching {WOW_EXE_PATH}")
        subprocess.Popen([WOW_EXE_PATH])
        log_message(f"Waiting {STARTUP_DELAY} seconds for WoW to start...")
        for i in range(STARTUP_DELAY):
            if emergency_stop: return
            time.sleep(1)
        
        # Step 2: Login
        log_message("Entering username...")
        type_string_with_delay(USERNAME, 0.5)
        press_key_with_delay('tab', 0.3)
        type_string_with_delay(PASSWORD, 0.3)
        press_key_with_delay('enter', 0.3)
        
        log_message(f"Waiting {LOGIN_DELAY} seconds for login...")
        for i in range(LOGIN_DELAY):
            if emergency_stop: return
            time.sleep(1)
        
        # Step 3: Character selection
        safe_click(COORD_CHARSELECT, "Character Select", 0.5)
        press_key_with_delay('enter', 0.5)
        
        log_message(f"Waiting {CHAR_SELECT_DELAY} seconds for world load...")
        for i in range(CHAR_SELECT_DELAY):
            if emergency_stop: return
            time.sleep(1)
        
        # Step 4: Mail interaction
        safe_click(COORD_MAIL, "Mailbox", 0.5)
        press_key_with_delay('g', 0.3)
        safe_click(COORD_MAILALL, "Mail All", 0.3)
        
        log_message(f"Waiting {MAIL_WAIT} seconds for mail...")
        for i in range(MAIL_WAIT):
            if emergency_stop: return
            time.sleep(1)
        
        # Step 5: First NPC interaction
        press_key_with_delay('1', 0.3)
        safe_click(COORD_NPCBANNER, "NPC Banner", 0.3)
        press_key_with_delay('g', 0.3)
        
        # Step 6: Restock
        safe_click(COORD_RESTOCK, "Restock", 0.3)
        log_message(f"Waiting {RESTOCK_WAIT} seconds...")
        for i in range(RESTOCK_WAIT):
            if emergency_stop: return
            time.sleep(1)
        
        # Step 7: Second NPC interaction with cancel routine
        press_key_with_delay('2', 0.3)
        safe_click(COORD_NPCBANNER, "NPC Banner", 0.3)
        press_key_with_delay('g', 0.3)
        
        safe_click(COORD_SCANCANCEL, "Scan Cancel", 0.3)
        
        log_message(f"Waiting {SCAN_WAIT} seconds...")
        for i in range(SCAN_WAIT):
            if emergency_stop: return
            time.sleep(1)
        
        # Step 8: 50x cancel clicks
        multi_click(COORD_CANCEL, CLICKS_50_COUNT, "Cancel Button", CLICK_DURATION, CLICK_BREAK)
        
        # Step 9: Shop interaction
        safe_click(COORD_TABSHOP, "Shop Tab", 0.3)
        safe_click(COORD_SHOPSEARCH, "Shop Search", 0.3)
        
        log_message(f"Waiting {SHOP_WAIT} seconds for shop search...")
        for i in range(SHOP_WAIT):
            if emergency_stop: return
            time.sleep(1)
        
        # Step 10: Buy top item 50x
        safe_click(COORD_SEARCHTOPITEM, "Search Top Item", 0.3)
        multi_click(COORD_SHOPBUY, CLICKS_50_COUNT, "Shop Buy", CLICK_DURATION, CLICK_BREAK)
        
        # Step 11: Reload UI
        press_key_with_delay('enter', 0.3)
        type_string_with_delay("/rl", 0.1)
        press_key_with_delay('enter', 0.3)
        
        log_message(f"Waiting {RL_WAIT} seconds after /rl...")
        for i in range(RL_WAIT):
            if emergency_stop: return
            time.sleep(1)
        
        # Step 12: Mail again
        safe_click(COORD_MAIL, "Mailbox", 0.3)
        press_key_with_delay('g', 0.3)
        safe_click(COORD_MAILALL, "Mail All", 0.3)
        log_message(f"Waiting {MAIL_WAIT} seconds...")
        for i in range(MAIL_WAIT):
            if emergency_stop: return
            time.sleep(1)
        
        # Step 13: Create scan
        press_key_with_delay('2', 0.3)
        safe_click(COORD_NPCBANNER, "NPC Banner", 0.3)
        press_key_with_delay('g', 0.3)
        
        safe_click(COORD_CREATESCAN, "Create Scan", 0.3)
        
        log_message(f"Waiting {CREATE_SCAN_WAIT} seconds for scan...")
        for i in range(CREATE_SCAN_WAIT):
            if emergency_stop: return
            time.sleep(1)
        
        # Step 14: Create post 50x
        multi_click(COORD_CREATEPOST, CLICKS_50_COUNT, "Create Post", CLICK_DURATION, CLICK_BREAK)
        
        # Step 15: Exit
        press_key_with_delay('5', 0.3)
        time.sleep(5)
        press_key_with_delay('enter', 0.3)
        type_string_with_delay("/beenden", 0.1)
        press_key_with_delay('enter', 0.3)
        
        log_message("Script completed successfully!")
        
    except Exception as e:
        log_message(f"ERROR: {e}")
        log_message("Script stopped due to error")
    finally:
        keyboard.remove_hotkey('f6')

if __name__ == "__main__":
    # Safety confirmation
    print("=" * 50)
    print("WARNING: This script will automate mouse/keyboard actions!")
    print("Make sure WoW is in WINDOWED MODE")
    print("Set all coordinates in the CONFIGURATION section first!")
    print("Press F6 at any time to emergency stop")
    print("=" * 50)
    confirm = input("Type 'YES' to continue: ")
    if confirm == "YES":
        main()
    else:
        print("Aborted.")
