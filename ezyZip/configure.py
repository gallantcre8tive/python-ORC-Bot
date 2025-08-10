import pytesseract
from PIL import Image
import pyautogui
import time
import pyperclip
import random
import os
import json
import keyboard
from datetime import datetime

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

CONFIG_PATH = "config.json"
SCREENSHOT_FOLDER = "screenshots"
os.makedirs(SCREENSHOT_FOLDER, exist_ok=True)

def load_config():
    with open(CONFIG_PATH, "r") as f:
        return json.load(f)

def save_config(config):
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=2)

def random_delay(min_delay, max_delay):
    delay = random.uniform(min_delay, max_delay)
    print(f"⏳ Waiting {delay:.2f} seconds...")
    time.sleep(delay)

def take_screenshot(region, filename):
    image = pyautogui.screenshot(region=region)
    image.save(filename)
    return filename

def extract_text(image_path):
    return pytesseract.image_to_string(Image.open(image_path))

def main():
    config = load_config()
    regions = config["regions"]
    region_key = config["active_region"]

    print("🤖 OCR Bot Started!")
    print("➡️ Press 'r' to switch region")
    print("➡️ Press 'Esc' to stop\n")

    try:
        while True:
            if keyboard.is_pressed("esc"):
                print("🛑 Bot stopped by user.")
                break

            if keyboard.is_pressed("r"):
                keys = list(regions.keys())
                index = keys.index(region_key)
                region_key = keys[(index + 1) % len(keys)]
                config["active_region"] = region_key
                save_config(config)
                print(f"🔁 Region switched to {region_key}")
                time.sleep(0.5)

            region = tuple(regions[region_key])
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = os.path.join(SCREENSHOT_FOLDER, f"question_{timestamp}.png")

            print(f"\n📸 Taking screenshot (region {region_key})...")
            take_screenshot(region, filename)

            print("🔍 Running OCR...")
            text = extract_text(filename).strip()
            print("📝 Extracted Text:\n", text)

            pyperclip.copy(text)
            print("✅ Text copied to clipboard.")

            random_delay(config["min_delay"], config["max_delay"])

    except KeyboardInterrupt:
        print("🛑 Bot interrupted.")

if __name__ == "__main__":
    main()
