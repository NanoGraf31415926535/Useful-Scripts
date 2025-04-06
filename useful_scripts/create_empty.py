import os
import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext

def create_items(create_type, base_directory, names, output_widget=None):
    """Creates empty files or folders in the specified directory."""
    base_directory = os.path.expanduser(base_directory)
    created_count = 0
    errors = []

    if not os.path.isdir(base_directory):
        if output_widget:
            output_widget.insert(tk.END, f"Error: Directory '{base_directory}' not found.\n")
        return created_count, ["Error: Base directory not found."]

    if output_widget:
        output_widget.insert(tk.END, f"Attempting to create {create_type}(s) in '{base_directory}'...\n")

    for name in names:
        full_path = os.path.join(base_directory, name)
        try:
            if create_type == 'file':
                with open(full_path, 'w'):
                    pass  # Create an empty file
                created_count += 1
                if output_widget:
                    output_widget.insert(tk.END, f"Created file: {full_path}\n")
            elif create_type == 'folder':
                os.makedirs(full_path, exist_ok=True)  # Create folder(s), no error if exists
                created_count += 1
                if output_widget:
                    output_widget.insert(tk.END, f"Created folder: {full_path}\n")
        except OSError as e:
            error_message = f"Error creating '{name}': {e}\n"
            errors.append(error_message)
            if output_widget:
                output_widget.insert(tk.END, error_message)

    return created_count, errors

def create_gui(parent):
    create_window = tk.Toplevel(parent)
    create_window.title("Create Empty Files/Folders")

    type_label = ttk.Label(create_window, text="Create:")
    type_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
    type_var = tk.StringVar(value="file")
    file_radio = ttk.Radiobutton(create_window, text="Files", variable=type_var, value="file")
    file_radio.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
    folder_radio = ttk.Radiobutton(create_window, text="Folders", variable=type_var, value="folder")
    folder_radio.grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)

    dir_label = ttk.Label(create_window, text="Base Directory:")
    dir_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
    dir_entry = ttk.Entry(create_window, width=40)
    dir_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.EW)

    def browse_directory():
        directory = filedialog.askdirectory(parent=create_window, initialdir=os.path.expanduser("~"), title="Select Directory")
        if directory:
            dir_entry.delete(0, tk.END)
            dir_entry.insert(0, directory)

    browse_button = ttk.Button(create_window, text="Browse", command=browse_directory)
    browse_button.grid(row=1, column=2, padx=5, pady=5, sticky=tk.E)

    names_label = ttk.Label(create_window, text="Names (comma-separated):")
    names_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
    names_entry = ttk.Entry(create_window, width=40)
    names_entry.grid(row=2, column=1, columnspan=2, padx=5, pady=5, sticky=tk.EW)

    results_text = scrolledtext.ScrolledText(create_window, height=5, wrap=tk.WORD)
    results_text.grid(row=3, column=0, columnspan=3, padx=5, pady=5, sticky=tk.NSEW)
    create_window.grid_columnconfigure(1, weight=1)
    create_window.grid_rowconfigure(3, weight=1)

    def perform_create():
        create_type = type_var.get()
        base_directory = dir_entry.get()
        names_str = names_entry.get()
        names = [name.strip() for name in names_str.split(',')]
        results_text.delete(1.0, tk.END)

        if not base_directory:
            results_text.insert(tk.END, "Please enter a base directory.\n")
            return
        if not names:
            results_text.insert(tk.END, "Please enter names for the files/folders.\n")
            return

        created_count, errors = create_items(create_type, base_directory, names, results_text)
        results_text.insert(tk.END, f"\nSuccessfully created {created_count} item(s).\n")
        if errors:
            results_text.insert(tk.END, "\n--- Errors Encountered ---\n")
            for error in errors:
                results_text.insert(tk.END, f"{error}\n")
            results_text.insert(tk.END, "---------------------------\n")

    create_button = ttk.Button(create_window, text="Create", command=perform_create)
    create_button.grid(row=4, column=1, padx=5, pady=10)