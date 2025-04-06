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

        self.create_widgets()

    def create_widgets(self):
        ttk.Label(self.master, text="Select a script to run:").pack(pady=10)

        ttk.Button(self.master, text="1. Start Desktop Monitoring", command=self.run_desktop_monitor).pack(pady=5, padx=20, fill=tk.X)
        ttk.Button(self.master, text="2. File Search", command=self.run_file_search).pack(pady=5, padx=20, fill=tk.X)
        ttk.Button(self.master, text="3. Duplicate File Finder", command=self.run_duplicate_finder).pack(pady=5, padx=20, fill=tk.X)
        ttk.Button(self.master, text="4. Bulk Rename Tool", command=self.run_bulk_rename).pack(pady=5, padx=20, fill=tk.X)
        ttk.Button(self.master, text="5. File Type Counter", command=self.run_file_type_counter).pack(pady=5, padx=20, fill=tk.X)
        ttk.Button(self.master, text="6. Create Empty Files/Folders", command=self.run_create_empty).pack(pady=5, padx=20, fill=tk.X)
        ttk.Button(self.master, text="7. System Info Display", command=self.run_system_info_gui).pack(pady=5, padx=20, fill=tk.X)
        ttk.Button(self.master, text="8. Network Speed Test", command=self.run_network_speed_test_gui).pack(pady=5, padx=20, fill=tk.X)
        ttk.Button(self.master, text="9. Clipboard History", command=self.run_clipboard_history_gui).pack(pady=5, padx=20, fill=tk.X)
        ttk.Button(self.master, text="10. Clear Temporary Files", command=self.run_clear_temp_gui).pack(pady=5, padx=20, fill=tk.X)
        ttk.Button(self.master, text="11. Clear Python Package Cache (pip)", command=self.run_clear_pip_cache_gui).pack(pady=5, padx=20, fill=tk.X)

        ttk.Separator(self.master).pack(pady=10, fill=tk.X, padx=10)

        ttk.Button(self.master, text="Exit", command=self.master.quit).pack(pady=10, padx=20, fill=tk.X)

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
    gui = UsefulScriptsGUI(root)
    root.mainloop()