import tkinter as tk
from tkinter import ttk
from useful_scripts import desktop_monitor
from useful_scripts import file_search
from useful_scripts import duplicate_finder
from useful_scripts import bulk_rename
from useful_scripts import file_type_counter
from useful_scripts import create_empty
from useful_scripts import system_info
from useful_scripts import network_speed_test
from useful_scripts import clipboard_history
from useful_scripts import clear_temp
from useful_scripts import clear_pip_cache

class UsefulScriptsGUI:
    def __init__(self, master):
        self.master = master
        master.title("Useful Scripts")

        self.buttons = {}  # Store buttons for hover effect
        self.style = ttk.Style()
        self.default_button_style = 'TButton'
        self.hover_button_style = 'Hover.TButton'
        self._configure_styles()

        self.create_widgets()

    def _configure_styles(self):
        self.style.configure(self.default_button_style, padding=15, font=('Arial', 16))
        self.style.configure('TLabel', padding=10, font=('Arial', 18))
        self.style.configure(self.hover_button_style, background='#e0e0e0')

    def create_widgets(self):
        ttk.Label(self.master, text="Select a script to run:").pack(pady=10)

        button_data = [
            ("1. Start Desktop Monitoring", self.run_desktop_monitor),
            ("2. File Search", self.run_file_search),
            ("3. Duplicate File Finder", self.run_duplicate_finder),
            ("4. Bulk Rename Tool", self.run_bulk_rename),
            ("5. File Type Counter", self.run_file_type_counter),
            ("6. Create Empty Files/Folders", self.run_create_empty),
            ("7. System Info Display", self.run_system_info_gui),
            ("8. Network Speed Test", self.run_network_speed_test_gui),
            ("9. Clipboard History", self.run_clipboard_history_gui),
            ("10. Clear Temporary Files", self.run_clear_temp_gui),
            ("11. Clear Python Package Cache (pip)", self.run_clear_pip_cache_gui),
            ("Exit", self.master.quit)
        ]

        for text, command in button_data:
            button = ttk.Button(self.master, text=text, command=command, style=self.default_button_style)
            button.pack(pady=5, padx=20, fill=tk.X)
            button.bind("<Enter>", self.on_enter)
            button.bind("<Leave>", self.on_leave)
            self.buttons[button] = self.default_button_style

        ttk.Separator(self.master).pack(pady=10, fill=tk.X, padx=10)

    def on_enter(self, event):
        event.widget.config(style=self.hover_button_style)

    def on_leave(self, event):
        event.widget.config(style=self.default_button_style)

    def run_desktop_monitor(self):
        desktop_monitor.create_gui(self.master)

    def run_file_search(self):
        file_search.create_gui(self.master)

    def run_duplicate_finder(self):
        duplicate_finder.create_gui(self.master)

    def run_bulk_rename(self):
        bulk_rename.create_gui(self.master)

    def run_file_type_counter(self):
        file_type_counter.create_gui(self.master)

    def run_create_empty(self):
        create_empty.create_gui(self.master)

    def run_system_info_gui(self):
        system_info.create_gui(self.master)

    def run_network_speed_test_gui(self):
        network_speed_test.create_gui(self.master)

    def run_clipboard_history_gui(self):
        clipboard_history.create_gui(self.master)

    def run_clear_temp_gui(self):
        clear_temp.create_gui(self.master)

    def run_clear_pip_cache_gui(self):
        clear_pip_cache.create_gui(self.master)

if __name__ == "__main__":
    root = tk.Tk()

    style = ttk.Style()
    print("Available Themes:", style.theme_names())
    style.theme_use('clam')

    gui = UsefulScriptsGUI(root)
    root.mainloop()