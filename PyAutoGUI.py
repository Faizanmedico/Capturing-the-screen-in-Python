import pyautogui
import datetime
import os

def take_screenshot_pyautogui(filename="screenshot.png", region=None):
    """
    Takes a screenshot using PyAutoGUI.

    Args:
        filename (str): The name to save the screenshot as.
                        If "screenshot.png", it will append a timestamp.
        region (tuple, optional): A 4-tuple (left, top, width, height)
                                  to specify a region. If None, captures
                                  the entire screen.
    Returns:
        str: The path to the saved screenshot file.
    """
    try:
        if filename == "screenshot.png":
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"screenshot_pyautogui_{timestamp}.png"

        # pyautogui.screenshot() returns a PIL Image object
        img = pyautogui.screenshot(region=region)
        img.save(filename)
        print(f"Screenshot saved to: {os.path.abspath(filename)}")
        return os.path.abspath(filename)
    except Exception as e:
        print(f"Error taking screenshot with PyAutoGUI: {e}")
        return None

if __name__ == "__main__":
    # Take a full-screen screenshot
    take_screenshot_pyautogui()

    # Take a screenshot of a specific region (left, top, width, height)
    # take_screenshot_pyautogui(filename="region_pyautogui_screenshot.png", region=(100, 100, 500, 300))