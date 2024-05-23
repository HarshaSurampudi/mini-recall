# capture_service.py
import time
import os
import pyautogui
from uuid import uuid4

save_folder = "to_process"
if not os.path.exists(save_folder):
    os.makedirs(save_folder)


def take_screenshot(save_folder):
    screenshot = pyautogui.screenshot()
    file_path = os.path.join(save_folder, f"{uuid4()}.png")
    screenshot.save(file_path)
    print(f"Screenshot saved to {file_path}")


def main():
    try:
        while True:
            take_screenshot(save_folder)
            time.sleep(30)
    except KeyboardInterrupt:
        print("Screenshot capturing stopped.")


if __name__ == "__main__":
    main()
