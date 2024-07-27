from app.spreadsheet_manager import SpreadSheetManager
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import date, timedelta

class GUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Josh Hansen's Epic Stock Tracker")
        self.root.geometry("400x500")

        self.spreadsheet_manager = SpreadSheetManager("B3DCQB3M4469Z8IV")

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        self.create_basic_input_frame()
        self.create_consecutive_change_frame()
        self.create_daily_threshold_frame()
        self.create_period_change_frame()

    def create_basic_input_frame(self):
        basic_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(basic_frame, text="Basic Input")

        ttk.Label(basic_frame, text="Stock Symbol:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.symbol_entry = ttk.Entry(basic_frame)
        self.symbol_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)
        self.symbol_entry.insert(0, "IBM")  # Default value

        ttk.Label(basic_frame, text="Start Date:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.start_date = DateEntry(basic_frame, width=12, background='darkblue', foreground='white', 
                                    date_pattern='yyyy-mm-dd', maxdate=date.today() - timedelta(days=2))
        self.start_date.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)
        self.start_date.set_date(date.today() - timedelta(days=30))  # Default value

        ttk.Label(basic_frame, text="End Date:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.end_date = DateEntry(basic_frame, width=12, background='darkblue', foreground='white', 
                                  date_pattern='yyyy-mm-dd', maxdate=date.today() - timedelta(days=1))
        self.end_date.grid(row=2, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)
        self.end_date.set_date(date.today())  # Default value

        basic_frame.columnconfigure(1, weight=1)
        self.start_date.bind("<<DateEntrySelected>>", self.update_end_date_min)

    def update_end_date_min(self, event):
        self.end_date.config(mindate=self.start_date.get_date())

    def create_consecutive_change_frame(self):
        cons_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(cons_frame, text="Consecutive Changes")

        ttk.Label(cons_frame, text="Consecutive Days:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.cons_days_entry = ttk.Entry(cons_frame)
        self.cons_days_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)
        self.cons_days_entry.insert(0, "5")  # Default value

        ttk.Label(cons_frame, text="Direction:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.cons_direction = tk.StringVar(value="positive")
        ttk.Radiobutton(cons_frame, text="Positive", variable=self.cons_direction, value="positive").grid(row=1, column=1, sticky=tk.W, padx=5, pady=2)
        ttk.Radiobutton(cons_frame, text="Negative", variable=self.cons_direction, value="negative").grid(row=2, column=1, sticky=tk.W, padx=5, pady=2)

        cons_frame.columnconfigure(1, weight=1)

    def create_daily_threshold_frame(self):
        daily_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(daily_frame, text="Daily Threshold")

        ttk.Label(daily_frame, text="Percent Threshold:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.daily_threshold_entry = ttk.Entry(daily_frame)
        self.daily_threshold_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)
        self.daily_threshold_entry.insert(0, "2.5")  # Default value

        ttk.Label(daily_frame, text="Direction:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.daily_direction = tk.StringVar(value="positive")
        ttk.Radiobutton(daily_frame, text="Higher", variable=self.daily_direction, value="positive").grid(row=1, column=1, sticky=tk.W, padx=5, pady=2)
        ttk.Radiobutton(daily_frame, text="Lower", variable=self.daily_direction, value="negative").grid(row=2, column=1, sticky=tk.W, padx=5, pady=2)

        daily_frame.columnconfigure(1, weight=1)

    def create_period_change_frame(self):
        period_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(period_frame, text="Period Change")

        ttk.Label(period_frame, text="Percent Threshold:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.period_threshold_entry = ttk.Entry(period_frame)
        self.period_threshold_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)
        self.period_threshold_entry.insert(0, "5")  # Default value

        ttk.Label(period_frame, text="Number of Days:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.period_days_entry = ttk.Entry(period_frame)
        self.period_days_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)
        self.period_days_entry.insert(0, "5")  # Default value

        period_frame.columnconfigure(1, weight=1)

    def validate_inputs(self):
        if not self.symbol_entry.get():
            messagebox.showerror("Error", "Stock Symbol is required")
            return False
        if not self.cons_days_entry.get():
            messagebox.showerror("Error", "Consecutive Days is required")
            return False
        if not self.daily_threshold_entry.get():
            messagebox.showerror("Error", "Daily Percent Threshold is required")
            return False
        if not self.period_threshold_entry.get():
            messagebox.showerror("Error", "Period Percent Threshold is required")
            return False
        if not self.period_days_entry.get():
            messagebox.showerror("Error", "Period Number of Days is required")
            return False
        
        try:
            float(self.daily_threshold_entry.get())
            float(self.period_threshold_entry.get())
            int(self.cons_days_entry.get())
            int(self.period_days_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Invalid numeric input")
            return False

        if self.start_date.get_date() >= self.end_date.get_date():
            messagebox.showerror("Error", "End Date must be after Start Date")
            return False

        return True

    def get_user_input(self):
        return {
            "symbol": self.symbol_entry.get(),
            "start_date": self.start_date.get_date(),
            "end_date": self.end_date.get_date(),
            "consecutive_change": {
                "days": int(self.cons_days_entry.get()),
                "direction": self.cons_direction.get()
            },
            "daily_threshold": {
                "percent": float(self.daily_threshold_entry.get()),
                "direction": self.daily_direction.get()
            },
            "period_change": {
                "percent": float(self.period_threshold_entry.get()),
                "days": int(self.period_days_entry.get())
            }
        }

    def fetch_data(self):
        if self.validate_inputs():
            user_input = self.get_user_input()
            self.spreadsheet_manager.process_and_open(user_input)
        else:
            print("Input validation failed")

    def run(self):
        self.fetch_button = ttk.Button(self.root, text="Fetch and Process Data", command=self.fetch_data)
        self.fetch_button.pack(pady=10)
        self.root.mainloop()
