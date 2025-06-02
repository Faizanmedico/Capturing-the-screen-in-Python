import tkinter as tk
from tkinter import messagebox
import time

class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quiz App")
        self.root.geometry("800x700") # Adjust size as needed
        self.root.resizable(False, False)
        self.root.configure(bg="#e0f7fa") # Light blue-green background

        self.questions = [
            {
                "question": "Q1: OOP ka pura naam kya hai?",
                "options": [
                    "Object-Oriented Programming",
                    "Object-Oriented Protocol",
                    "Object-Oriented Process",
                    "Object-Oriented Paradigm"
                ],
                "answer": "Object-Oriented Programming"
            },
            {
                "question": "Q2: OOP mein 'Class' kya hai?",
                "options": [
                    "Ek function ka naam",
                    "Ek blueprint ya template",
                    "Ek variable type",
                    "Ek library"
                ],
                "answer": "Ek blueprint ya template"
            },
            {
                "question": "Q3: Python kis type ki programming language hai?",
                "options": [
                    "Procedural",
                    "Functional",
                    "Object-Oriented",
                    "Sabhi"
                ],
                "answer": "Sabhi"
            },
            {
                "question": "Q4: HTML ka pura naam kya hai?",
                "options": [
                    "HyperText Markup Language",
                    "High-level Text Machine Language",
                    "Hyperlink and Text Markup Language",
                    "Home Tool Markup Language"
                ],
                "answer": "HyperText Markup Language"
            },
            {
                "question": "Q5: CSS ka kya kaam hai?",
                "options": [
                    "Web content banana",
                    "Web content ko style karna",
                    "Web server chalana",
                    "Database manage karna"
                ],
                "answer": "Web content ko style karna"
            }
        ]

        self.current_question_index = 0
        self.score = 0
        self.total_time_per_question = 35 # seconds per question for simplicity
        self.time_left = self.total_time_per_question
        self.timer_running = False

        self.create_widgets()
        self.display_question()
        self.start_timer()

    def create_widgets(self):
        # Main container frame (mimics the white card in your image)
        self.main_frame = tk.Frame(self.root, bg="white", bd=2, relief="solid", padx=20, pady=20)
        self.main_frame.pack(pady=50, padx=50, fill="both", expand=True)

        # Quiz App Title
        self.title_label = tk.Label(self.main_frame, text="Quiz App", font=("Arial", 28, "bold"), fg="#8e24aa", bg="white")
        self.title_label.pack(pady=(10, 5))

        # Time Left label
        self.time_label = tk.Label(self.main_frame, text=f"Time Left: {self.time_left}:00", font=("Arial", 16), fg="#d32f2f", bg="white")
        self.time_label.pack(pady=(0, 15))

        # Progress bar for timer (Tkinter's default is simple, styling can be done with ttk)
        # For a more modern look like your image, you'd use ttk.Progressbar
        # self.progress_bar = ttk.Progressbar(self.main_frame, orient="horizontal", length=300, mode="determinate")
        # self.progress_bar.pack(pady=5)
        # self.progress_bar["maximum"] = self.total_time_per_question

        # Simple timer bar using a canvas for custom styling (closer to your image)
        self.timer_canvas = tk.Canvas(self.main_frame, width=400, height=15, bg="#eceff1", highlightthickness=0)
        self.timer_canvas.pack(pady=10)
        self.timer_rect = self.timer_canvas.create_rectangle(0, 0, self.timer_canvas.winfo_width(), 15, fill="#2196f3", outline="")


        # Question container frame
        self.question_frame = tk.Frame(self.main_frame, bg="#e3f2fd", bd=1, relief="solid", padx=15, pady=15)
        self.question_frame.pack(pady=20, fill="x")

        self.question_label = tk.Label(self.question_frame, text="", font=("Arial", 18), bg="#e3f2fd", wraplength=600)
        self.question_label.pack(pady=(0, 10))

        self.option_var = tk.StringVar()
        self.option_buttons = []
        for i in range(4): # For 4 options
            radio_btn = tk.Radiobutton(self.question_frame, text="", variable=self.option_var, value="",
                                       font=("Arial", 14), bg="#e3f2fd", selectcolor="#bbdefb",
                                       command=self.enable_submit_button)
            radio_btn.pack(anchor="w", pady=5)
            self.option_buttons.append(radio_btn)

        # Navigation Buttons
        self.button_frame = tk.Frame(self.main_frame, bg="white")
        self.button_frame.pack(pady=20)

        self.submit_button = tk.Button(self.button_frame, text="Submit Answer", command=self.submit_answer,
                                       font=("Arial", 14), bg="#4caf50", fg="white", state="disabled", padx=10, pady=5)
        self.submit_button.pack(side="left", padx=10)

        self.next_button = tk.Button(self.button_frame, text="Next Question", command=self.next_question,
                                     font=("Arial", 14), bg="#2196f3", fg="white", state="disabled", padx=10, pady=5)
        self.next_button.pack(side="left", padx=10)

    def display_question(self):
        if self.current_question_index < len(self.questions):
            self.timer_running = False # Stop current timer
            self.time_left = self.total_time_per_question # Reset time
            self.update_timer_display()
            self.start_timer() # Start new timer

            question_data = self.questions[self.current_question_index]
            self.question_label.config(text=question_data["question"])

            self.option_var.set("") # Clear previous selection
            self.submit_button.config(state="disabled") # Disable submit until an option is chosen
            self.next_button.config(state="disabled") # Disable next button until submit

            for i, option_text in enumerate(question_data["options"]):
                self.option_buttons[i].config(text=option_text, value=option_text)
            self.enable_radio_buttons()
        else:
            self.end_quiz()

    def enable_radio_buttons(self):
        for btn in self.option_buttons:
            btn.config(state="normal")

    def disable_radio_buttons(self):
        for btn in self.option_buttons:
            btn.config(state="disabled")

    def enable_submit_button(self):
        # Enable submit only if an option is selected
        if self.option_var.get():
            self.submit_button.config(state="normal")
        else:
            self.submit_button.config(state="disabled")

    def submit_answer(self):
        self.timer_running = False # Stop the timer when submitted
        selected_answer = self.option_var.get()
        correct_answer = self.questions[self.current_question_index]["answer"]

        self.disable_radio_buttons() # Prevent changing answer after submission
        self.submit_button.config(state="disabled") # Disable submit button

        if selected_answer == correct_answer:
            self.score += 1
            messagebox.showinfo("Result", "Correct Answer!")
        else:
            messagebox.showinfo("Result", f"Wrong Answer! Correct answer was: {correct_answer}")

        self.next_button.config(state="normal") # Enable next button

    def next_question(self):
        self.current_question_index += 1
        self.display_question()

    def start_timer(self):
        self.timer_running = True
        self.update_timer()

    def update_timer_display(self):
        # Update time label
        minutes = self.time_left // 60
        seconds = self.time_left % 60
        self.time_label.config(text=f"Time Left: {minutes:02d}:{seconds:02d}")

        # Update timer bar
        progress_width = (self.time_left / self.total_time_per_question) * self.timer_canvas.winfo_width()
        self.timer_canvas.coords(self.timer_rect, 0, 0, progress_width, 15)

        # Change color based on remaining time (optional, for visual feedback)
        if self.time_left > self.total_time_per_question / 2:
            self.timer_canvas.itemconfig(self.timer_rect, fill="#2196f3") # Blue
        elif self.time_left > self.total_time_per_question / 4:
            self.timer_canvas.itemconfig(self.timer_rect, fill="#ffeb3b") # Yellow
        else:
            self.timer_canvas.itemconfig(self.timer_rect, fill="#f44336") # Red


    def update_timer(self):
        if self.timer_running and self.time_left > 0:
            self.time_left -= 1
            self.update_timer_display()
            self.root.after(1000, self.update_timer) # Call itself after 1 second
        elif self.time_left == 0 and self.timer_running:
            self.timer_running = False
            messagebox.showinfo("Time's Up!", "Time's up for this question!")
            self.submit_answer() # Automatically submit if time runs out (will count as wrong if nothing selected)
            if self.next_button['state'] == 'disabled': # If user didn't select an answer and time ran out
                 self.next_question() # Automatically move to next question


    def end_quiz(self):
        self.timer_running = False # Stop the timer
        messagebox.showinfo("Quiz Finished", f"Quiz Completed!\nYour score: {self.score}/{len(self.questions)}")
        self.root.destroy() # Close the application

if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()