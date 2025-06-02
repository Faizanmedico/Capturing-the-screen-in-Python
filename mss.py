import mss
import mss.tools
import datetime
import os

def take_screenshot_mss(filename="screenshot.png", monitor_number=1, region=None):
    """
    Takes a screenshot using the mss library.

    Args:
        filename (str): The name to save the screenshot as.
                        If "screenshot.png", it will append a timestamp.
        monitor_number (int): The monitor to capture (1 for primary, 0 for all).
        region (dict, optional): A dictionary like {"top": Y, "left": X, "width": W, "height": H}
                                 to specify a region. If None, captures the entire monitor.
    Returns:
        str: The path to the saved screenshot file.
    """
    try:
        with mss.mss() as sct:
            if filename == "screenshot.png":
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"screenshot_mss_{timestamp}.png"

            if region:
                # Capture a specific region
                sct_img = sct.grab(region)
            else:
                # Capture a specific monitor or all monitors
                # sct.monitors[0] is for all monitors, sct.monitors[1] is for the first
                # Check sct.monitors to see available monitor indices
                if monitor_number == 0: # Capture all monitors
                    monitor_to_grab = sct.monitors[0]
                else: # Capture a specific monitor (e.g., primary)
                    if len(sct.monitors) > monitor_number:
                        monitor_to_grab = sct.monitors[monitor_number]
                    else:
                        print(f"Monitor {monitor_number} not found. Capturing primary monitor.")
                        monitor_to_grab = sct.monitors[1] # Fallback to primary

                sct_img = sct.grab(monitor_to_grab)

            # Save to the picture file
            mss.tools.to_png(sct_img.rgb, sct_img.size, output=filename)
            print(f"Screenshot saved to: {os.path.abspath(filename)}")
            return os.path.abspath(filename)

    except Exception as e:
        print(f"Error taking screenshot with mss: {e}")
        return None

if __name__ == "__main__":
    # Take a full-screen screenshot of the primary monitor
    take_screenshot_mss()

    # Take a screenshot of a specific region using mss
    # region_coords = {"top": 100, "left": 100, "width": 500, "height": 300}
    # take_screenshot_mss(filename="region_mss_screenshot.png", region=region_coords)