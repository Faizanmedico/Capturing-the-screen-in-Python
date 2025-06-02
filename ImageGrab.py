from PIL import ImageGrab
import datetime
import os

def take_screenshot_pil(filename="screenshot.png", region=None):
    """
    Takes a screenshot using Pillow's ImageGrab.

    Args:
        filename (str): The name to save the screenshot as.
                        If "screenshot.png", it will append a timestamp.
        region (tuple, optional): A 4-tuple (left, top, right, bottom)
                                  to specify a region. If None, captures
                                  the entire screen.
    Returns:
        str: The path to the saved screenshot file.
    """
    try:
        if filename == "screenshot.png":
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"screenshot_{timestamp}.png"

        img = ImageGrab.grab(bbox=region)
        img.save(filename)
        print(f"Screenshot saved to: {os.path.abspath(filename)}")
        return os.path.abspath(filename)
    except Exception as e:
        print(f"Error taking screenshot with Pillow: {e}")
        return None

if __name__ == "__main__":
    # Take a full-screen screenshot
    take_screenshot_pil()

    # Take a screenshot of a specific region (e.g., top-left 800x600 pixels)
    # You'll need to adjust these coordinates for your screen.
    # On Windows, you can use tools like "Snipping Tool" to get coordinates.
    # For a cross-platform solution, a more robust region selection GUI is needed.
    # take_screenshot_pil(filename="region_screenshot.png", region=(0, 0, 800, 600))