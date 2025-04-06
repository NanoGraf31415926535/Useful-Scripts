import os
from collections import defaultdict
import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext

def count_file_types(search_directory, include_subdirectories=False, output_widget=None):
    """Counts the occurrences of each file type in the specified directory."""
    file_type_counts = defaultdict(int)

    if not os.path.isdir(search_directory):
        if output_widget:
            output_widget.insert(tk.END, f"Error: Directory '{search_directory}' not found.\n")
        return file_type_counts

    if output_widget:
        output_widget.insert(tk.END, f"Scanning directory: '{search_directory}'...\n")
        if include_subdirectories:
            output_widget.insert(tk.END, "Including subdirectories.\n")

    walk = os.walk(search_directory) if include_subdirectories else [(search_directory, [], os.listdir(search_directory))]

    for root, _, filenames in walk:
        for filename in filenames:
            if os.path.isfile(os.path.join(root, filename)):
                _, extension = os.path.splitext(filename)
                if extension:
                    file_type_counts[extension.lower()] += 1

    if not file_type_counts and output_widget:
        output_widget.insert(tk.END, f"No files found in '{search_directory}' (and subdirectories if specified).\n")
    elif output_widget:
        output_widget.insert(tk.END, "\n--- File Type Counts ---\n")
        for file_type, count in sorted(file_type_counts.items()):
            output_widget.insert(tk.END, f"{file_type}: {count}\n")
        output_widget.insert(tk.END, "-------------------------\n")

    return file_type_counts

def create_gui(parent):
    counter_window = tk.Toplevel(parent)
    counter_window.title("File Type Counter")

    ttk.Label(counter_window, text="Directory to Scan:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
    dir_entry = ttk.Entry(counter_window, width=40)
    dir_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.EW)

    def browse_directory():
        directory = filedialog.askdirectory(parent=counter_window, initialdir=os.path.expanduser("~"), title="Select Directory")
        if directory:
            dir_entry.delete(0, tk.END)
            dir_entry.insert(0, directory)

    browse_button = ttk.Button(counter_window, text="Browse", command=browse_directory)
    browse_button.grid(row=0, column=2, padx=5, pady=5, sticky=tk.E)

    include_sub_var = tk.BooleanVar()
    include_sub_check = ttk.Checkbutton(counter_window, text="Include Subdirectories", variable=include_sub_var)
    include_sub_check.grid(row=1, column=0, columnspan=3, padx=5, pady=5, sticky=tk.W)

    results_frame = ttk.LabelFrame(counter_window, text="File Type Counts")
    results_frame.grid(row=2, column=0, columnspan=3, padx=5, pady=5, sticky=tk.NSEW)
    counter_window.grid_columnconfigure(1, weight=1)
    counter_window.grid_rowconfigure(2, weight=1)

    results_text = scrolledtext.ScrolledText(results_frame, height=10, wrap=tk.WORD)
    results_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def perform_count():
        search_directory = dir_entry.get()
        include_subdirectories = include_sub_var.get()
        results_text.delete(1.0, tk.END)

        if not search_directory:
            results_text.insert(tk.END, "Please enter a directory to scan.\n")
            return

        count_file_types(search_directory, include_subdirectories, results_text)

    count_button = ttk.Button(counter_window, text="Count File Types", command=perform_count)
    count_button.grid(row=3, column=1, padx=5, pady=10)