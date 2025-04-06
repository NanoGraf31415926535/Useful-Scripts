import os
import hashlib
import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext

def calculate_hash(file_path, hash_algorithm='md5'):
    """Calculates the hash of a file's content."""
    hasher = hashlib.new(hash_algorithm)
    try:
        with open(file_path, 'rb') as file:
            while chunk := file.read(4096):
                hasher.update(chunk)
        return hasher.hexdigest()
    except FileNotFoundError:
        return None
    except PermissionError:
        print(f"Permission denied to read: {file_path}")
        return None

def find_duplicates(search_directory, include_subdirectories=False, output_widget=None):
    """Finds duplicate files within the specified directory and updates the output widget."""
    files_by_size = {}
    duplicates = {}

    if not os.path.isdir(search_directory):
        if output_widget:
            output_widget.insert(tk.END, f"Error: Directory '{search_directory}' not found.\n")
        return {}

    if output_widget:
        output_widget.insert(tk.END, f"Scanning for duplicate files in '{search_directory}'...\n")
        if include_subdirectories:
            output_widget.insert(tk.END, "Including subdirectories...\n")

    walk = os.walk(search_directory) if include_subdirectories else [(search_directory, [], os.listdir(search_directory))]

    for root, _, filenames in walk:
        for filename in filenames:
            file_path = os.path.join(root, filename)
            try:
                file_size = os.path.getsize(file_path)
                if file_size > 0:  # Ignore empty files for now
                    if file_size not in files_by_size:
                        files_by_size[file_size] = []
                    files_by_size[file_size].append(file_path)
            except OSError as e:
                if output_widget:
                    output_widget.insert(tk.END, f"Error getting size for {file_path}: {e}\n")

    for size, file_list in files_by_size.items():
        if len(file_list) > 1:
            files_by_hash = {}
            for file_path in file_list:
                file_hash = calculate_hash(file_path)
                if file_hash:
                    if file_hash not in files_by_hash:
                        files_by_hash[file_hash] = []
                    files_by_hash[file_hash].append(file_path)

            for hash_value, duplicate_group in files_by_hash.items():
                if len(duplicate_group) > 1:
                    hash_key = f"duplicates_{hash_value}"
                    duplicates[hash_key] = duplicate_group
                    if output_widget:
                        output_widget.insert(tk.END, f"\n--- Duplicate Group ---\n")
                        for file_path in duplicate_group:
                            output_widget.insert(tk.END, f"- {file_path}\n")

    if not duplicates and output_widget:
        output_widget.insert(tk.END, "No duplicate files found.\n")
    elif duplicates and output_widget:
        output_widget.insert(tk.END, "\n-----------------------\n")

    return duplicates

def create_gui(parent):
    duplicate_window = tk.Toplevel(parent)
    duplicate_window.title("Duplicate File Finder")

    ttk.Label(duplicate_window, text="Search Directory:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
    dir_entry = ttk.Entry(duplicate_window, width=40)
    dir_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.EW)

    def browse_directory():
        directory = filedialog.askdirectory(parent=duplicate_window, initialdir=os.path.expanduser("~"), title="Select Directory")
        if directory:
            dir_entry.delete(0, tk.END)
            dir_entry.insert(0, directory)

    browse_button = ttk.Button(duplicate_window, text="Browse", command=browse_directory)
    browse_button.grid(row=0, column=2, padx=5, pady=5, sticky=tk.E)

    include_sub_var = tk.BooleanVar()
    include_sub_check = ttk.Checkbutton(duplicate_window, text="Include Subdirectories", variable=include_sub_var)
    include_sub_check.grid(row=1, column=0, columnspan=3, padx=5, pady=5, sticky=tk.W)

    results_frame = ttk.LabelFrame(duplicate_window, text="Duplicate Files Found")
    results_frame.grid(row=2, column=0, columnspan=3, padx=5, pady=5, sticky=tk.NSEW)
    duplicate_window.grid_columnconfigure(1, weight=1)
    duplicate_window.grid_rowconfigure(2, weight=1)

    results_text = scrolledtext.ScrolledText(results_frame, height=10, wrap=tk.WORD)
    results_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def perform_duplicate_find():
        search_directory = dir_entry.get()
        include_subdirectories = include_sub_var.get()
        results_text.delete(1.0, tk.END)  # Clear previous results

        if not search_directory:
            results_text.insert(tk.END, "Please enter a directory to search.\n")
            return

        find_duplicates(search_directory, include_subdirectories, results_text)

    find_button = ttk.Button(duplicate_window, text="Find Duplicates", command=perform_duplicate_find)
    find_button.grid(row=3, column=1, padx=5, pady=10)