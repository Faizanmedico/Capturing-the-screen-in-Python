import tkinter as tk
from tkinter import filedialog, messagebox, Toplevel
from PIL import Image, ImageTk
import mss
import datetime
import os
import io

class ScreenCaptureApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Screen Capture Tool")
        self.root.geometry("400x300")
        self.root.resizable(False, False)
        self.root.configure(bg="#f0f0f0")

        self.last_screenshot_path = None

        self.create_widgets()

    def create_widgets(self):
        # Title Label
        title_label = tk.Label(self.root, text="Python Screen Capture",
                               font=("Arial", 16, "bold"), bg="#f0f0f0", fg="#333333")
        title_label.pack(pady=20)

        # Full Screen Capture Button
        full_screen_button = tk.Button(self.root, text="Capture Full Screen",
                                      command=self.capture_full_screen,
                                      font=("Arial", 12), bg="#4CAF50", fg="white",
                                      padx=10, pady=5, relief="raised")
        full_screen_button.pack(pady=10)

        # Region Capture Button (simplified: will ask for coordinates)
        region_capture_button = tk.Button(self.root, text="Capture Region (Manual Coords)",
                                         command=self.show_region_input,
                                         font=("Arial", 12), bg="#2196F3", fg="white",
                                         padx=10, pady=5, relief="raised")
        region_capture_button.pack(pady=10)

        # View Last Screenshot Button
        view_button = tk.Button(self.root, text="View Last Screenshot",
                                command=self.view_last_screenshot,
                                font=("Arial", 12), bg="#FFC107", fg="black",
                                padx=10, pady=5, relief="raised")
        view_button.pack(pady=10)

        # Status Label
        self.status_label = tk.Label(self.root, text="Ready", font=("Arial", 10), bg="#f0f0f0", fg="#555555")
        self.status_label.pack(pady=10)

    def capture_full_screen(self):
        self.status_label.config(text="Capturing full screen...")
        self.root.update_idletasks() # Update GUI immediately

        # Hide the main window briefly to prevent it from being in the screenshot
        self.root.withdraw()

        try:
            with mss.mss() as sct:
                # Get information of the primary monitor
                monitor = sct.monitors[1]
                sct_img = sct.grab(monitor)

                # Convert to PIL Image
                img = Image.frombytes("RGB", sct_img.size, sct_img.rgb)

                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"full_screenshot_{timestamp}.png"

                save_path = filedialog.asksaveasfilename(
                    defaultextension=".png",
                    filetypes=[("PNG files", "*.png"), ("All files", "*.*")],
                    initialfile=filename
                )

                if save_path:
                    img.save(save_path)
                    self.last_screenshot_path = save_path
                    self.status_label.config(text=f"Full screenshot saved to: {os.path.basename(save_path)}")
                else:
                    self.status_label.config(text="Screenshot capture cancelled.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to capture full screen:\n{e}")
            self.status_label.config(text="Error capturing screen.")
        finally:
            # Bring the main window back
            self.root.deiconify()


    def show_region_input(self):
        # Create a new Toplevel window for region input
        region_window = Toplevel(self.root)
        region_window.title("Enter Region Coordinates")
        region_window.geometry("300x200")
        region_window.transient(self.root) # Make it appear on top of the main window
        region_window.grab_set() # Make it modal

        tk.Label(region_window, text="Left:").pack(pady=5)
        left_entry = tk.Entry(region_window)
        left_entry.pack()
        left_entry.insert(0, "0")

        tk.Label(region_window, text="Top:").pack(pady=5)
        top_entry = tk.Entry(region_window)
        top_entry.pack()
        top_entry.insert(0, "0")

        tk.Label(region_window, text="Width:").pack(pady=5)
        width_entry = tk.Entry(region_window)
        width_entry.pack()
        width_entry.insert(0, "800")

        tk.Label(region_window, text="Height:").pack(pady=5)
        height_entry = tk.Entry(region_window)
        height_entry.pack()
        height_entry.insert(0, "600")

        def capture_with_coords():
            try:
                left = int(left_entry.get())
                top = int(top_entry.get())
                width = int(width_entry.get())
                height = int(height_entry.get())

                region_coords = {"top": top, "left": left, "width": width, "height": height}
                region_window.destroy() # Close input window

                self.capture_region_screen(region_coords)

            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter valid integer coordinates.")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")

        capture_button = tk.Button(region_window, text="Capture", command=capture_with_coords,
                                   bg="#4CAF50", fg="white", padx=10, pady=5)
        capture_button.pack(pady=15)


    def capture_region_screen(self, region_coords):
        self.status_label.config(text=f"Capturing region: {region_coords}...")
        self.root.update_idletasks() # Update GUI immediately

        self.root.withdraw() # Hide the main window

        try:
            with mss.mss() as sct:
                sct_img = sct.grab(region_coords)
                img = Image.frombytes("RGB", sct_img.size, sct_img.rgb)

                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"region_screenshot_{timestamp}.png"

                save_path = filedialog.asksaveasfilename(
                    defaultextension=".png",
                    filetypes=[("PNG files", "*.png"), ("All files", "*.*")],
                    initialfile=filename
                )

                if save_path:
                    img.save(save_path)
                    self.last_screenshot_path = save_path
                    self.status_label.config(text=f"Region screenshot saved to: {os.path.basename(save_path)}")
                else:
                    self.status_label.config(text="Region screenshot cancelled.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to capture region:\n{e}")
            self.status_label.config(text="Error capturing region.")
        finally:
            self.root.deiconify()

    def view_last_screenshot(self):
        if not self.last_screenshot_path or not os.path.exists(self.last_screenshot_path):
            messagebox.showinfo("No Screenshot", "No screenshot has been taken yet or file not found.")
            return

        try:
            img = Image.open(self.last_screenshot_path)
            img.show() # Uses default image viewer
            self.status_label.config(text=f"Opened: {os.path.basename(self.last_screenshot_path)}")
        except Exception as e:
            messagebox.showerror("Error", f"Could not open image:\n{e}")
            self.status_label.config(text="Error viewing screenshot.")


if __name__ == "__main__":
    root = tk.Tk()
    app = ScreenCaptureApp(root)
    root.mainloop()