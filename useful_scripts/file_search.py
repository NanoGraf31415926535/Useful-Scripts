import os
import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext

def search_files(search_query, search_directory, output_widget):
    """
    Searches for files containing the search query within the specified directory
    and updates the output widget.

    Args:
        search_query (str): The filename or part of the name to search for.
        search_directory (str): The directory to search within.
        output_widget (tk.scrolledtext.ScrolledText): The widget to display results.
    """
    search_directory = os.path.expanduser(search_directory)

    if not os.path.isdir(search_directory):
        output_widget.insert(tk.END, f"Error: Directory '{search_directory}' not found.\n")
        return

    output_widget.insert(tk.END, f"Searching for files containing '{search_query}' in '{search_directory}'...\n")
    found_files = False
    for root, _, files in os.walk(search_directory):
        for name in files:
            if search_query.lower() in name.lower():
                full_path = os.path.join(root, name)
                output_widget.insert(tk.END, f"Found: {full_path}\n")
                found_files = True

    if not found_files:
        output_widget.insert(tk.END, "No files found matching your query.\n")

def create_gui(parent):
    search_window = tk.Toplevel(parent)
    search_window.title("File Search")

    ttk.Label(search_window, text="Search Query:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
    query_entry = ttk.Entry(search_window, width=40)
    query_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.EW)

    ttk.Label(search_window, text="Search Directory:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
    dir_entry = ttk.Entry(search_window, width=40)
    dir_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.EW)

    def browse_directory():
        directory = filedialog.askdirectory(parent=search_window, initialdir=os.path.expanduser("~"), title="Select Directory")
        if directory:
            dir_entry.delete(0, tk.END)
            dir_entry.insert(0, directory)

    browse_button = ttk.Button(search_window, text="Browse", command=browse_directory)
    browse_button.grid(row=1, column=2, padx=5, pady=5, sticky=tk.E)

    results_frame = ttk.LabelFrame(search_window, text="Search Results")
    results_frame.grid(row=2, column=0, columnspan=3, padx=5, pady=5, sticky=tk.NSEW)
    search_window.grid_columnconfigure(1, weight=1)
    search_window.grid_rowconfigure(2, weight=1)

    results_text = scrolledtext.ScrolledText(results_frame, height=10, wrap=tk.WORD)
    results_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def perform_search():
        query = query_entry.get()
        directory = dir_entry.get()
        results_text.delete(1.0, tk.END)  # Clear previous results
        if not query or not directory:
            results_text.insert(tk.END, "Please enter both a search query and a directory.\n")
            return

        search_files(query, directory, results_text)

    search_button = ttk.Button(search_window, text="Search", command=perform_search)
    search_button.grid(row=3, column=1, padx=5, pady=10)