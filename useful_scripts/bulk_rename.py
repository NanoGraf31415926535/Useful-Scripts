# bulk_rename.py

import os
import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext, messagebox

def get_files_to_rename(directory):
    """Returns a list of files in the given directory."""
    if not os.path.isdir(directory):
        raise FileNotFoundError(f"Directory '{directory}' not found.")
    return [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

def preview_rename_actions(files_to_rename, operation, prefix="", string_to_replace="", replacement_string=""):
    """Previews the renaming actions."""
    rename_actions = []
    for filename in files_to_rename:
        new_name = filename
        if operation == 'prefix':
            new_name = prefix + filename
        elif operation == 'replace':
            new_name = filename.replace(string_to_replace, replacement_string)
        if new_name != filename:
            rename_actions.append((filename, new_name))
    return rename_actions

def perform_bulk_rename(rename_directory, operation, prefix="", string_to_replace="", replacement_string="", output_widget=None):
    """Performs the bulk renaming operation."""
    rename_directory = os.path.expanduser(rename_directory)
    renamed_count = 0
    errors = []

    try:
        files_to_rename = get_files_to_rename(rename_directory)
        rename_actions = preview_rename_actions(files_to_rename, operation, prefix, string_to_replace, replacement_string)

        if not rename_actions:
            if output_widget:
                output_widget.insert(tk.END, "No files to rename based on the criteria.\n")
            return 0

        for old_name, new_name in rename_actions:
            old_path = os.path.join(rename_directory, old_name)
            new_path = os.path.join(rename_directory, new_name)
            try:
                os.rename(old_path, new_path)
                renamed_count += 1
                if output_widget:
                    output_widget.insert(tk.END, f"Renamed: {old_name} -> {new_name}\n")
            except OSError as e:
                error_message = f"Error renaming '{old_name}' to '{new_name}': {e}\n"
                errors.append(error_message)
                if output_widget:
                    output_widget.insert(tk.END, error_message)

        return renamed_count

    except FileNotFoundError as e:
        raise e
    except Exception as e:
        if output_widget:
            output_widget.insert(tk.END, f"An unexpected error occurred: {e}\n")
        return 0

def create_gui(parent):
    rename_window = tk.Toplevel(parent)
    rename_window.title("Bulk Rename Tool")

    ttk.Label(rename_window, text="Directory to Rename:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
    dir_entry = ttk.Entry(rename_window, width=40)
    dir_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.EW)

    def browse_directory():
        directory = filedialog.askdirectory(parent=rename_window, initialdir=os.path.expanduser("~"), title="Select Directory")
        if directory:
            dir_entry.delete(0, tk.END)
            dir_entry.insert(0, directory)

    browse_button = ttk.Button(rename_window, text="Browse", command=browse_directory)
    browse_button.grid(row=0, column=2, padx=5, pady=5, sticky=tk.E)

    operation_label = ttk.Label(rename_window, text="Choose Operation:")
    operation_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
    operation_var = tk.StringVar(value="prefix")
    prefix_radio = ttk.Radiobutton(rename_window, text="Add Prefix", variable=operation_var, value="prefix")
    prefix_radio.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
    replace_radio = ttk.Radiobutton(rename_window, text="Replace String", variable=operation_var, value="replace")
    replace_radio.grid(row=1, column=2, padx=5, pady=5, sticky=tk.W)

    prefix_frame = ttk.LabelFrame(rename_window, text="Prefix Settings")
    prefix_frame.grid(row=2, column=0, columnspan=3, padx=5, pady=5, sticky=tk.EW)
    prefix_label = ttk.Label(prefix_frame, text="Prefix to Add:")
    prefix_label.pack(padx=5, pady=5, anchor=tk.W)
    prefix_entry = ttk.Entry(prefix_frame, width=40)
    prefix_entry.pack(padx=5, pady=5, fill=tk.X)
    prefix_frame.columnconfigure(1, weight=1)

    replace_frame = ttk.LabelFrame(rename_window, text="Replace Settings")
    replace_frame.grid(row=3, column=0, columnspan=3, padx=5, pady=5, sticky=tk.EW)
    replace_from_label = ttk.Label(replace_frame, text="String to Replace:")
    replace_from_label.pack(padx=5, pady=5, anchor=tk.W)
    replace_from_entry = ttk.Entry(replace_frame, width=40)
    replace_from_entry.pack(padx=5, pady=5, fill=tk.X)
    replace_to_label = ttk.Label(replace_frame, text="Replacement String:")
    replace_to_label.pack(padx=5, pady=5, anchor=tk.W)
    replace_to_entry = ttk.Entry(replace_frame, width=40)
    replace_to_entry.pack(padx=5, pady=5, fill=tk.X)
    replace_frame.columnconfigure(1, weight=1)

    # Initially show only the prefix frame
    replace_frame.grid_forget()

    def toggle_operation_settings(*args):
        if operation_var.get() == "prefix":
            prefix_frame.grid(row=2, column=0, columnspan=3, padx=5, pady=5, sticky=tk.EW)
            replace_frame.grid_forget()
        elif operation_var.get() == "replace":
            prefix_frame.grid_forget()
            replace_frame.grid(row=2, column=0, columnspan=3, padx=5, pady=5, sticky=tk.EW)

    operation_var.trace_add("write", toggle_operation_settings)

    preview_frame = ttk.LabelFrame(rename_window, text="Rename Preview")
    preview_frame.grid(row=4, column=0, columnspan=3, padx=5, pady=5, sticky=tk.NSEW)
    rename_window.grid_columnconfigure(1, weight=1)
    rename_window.grid_rowconfigure(4, weight=1)
    preview_text = scrolledtext.ScrolledText(preview_frame, height=8, wrap=tk.WORD)
    preview_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def perform_preview():
        rename_directory = dir_entry.get()
        operation = operation_var.get()
        prefix = prefix_entry.get()
        string_to_replace = replace_from_entry.get()
        replacement_string = replace_to_entry.get()
        preview_text.delete(1.0, tk.END)

        if not rename_directory:
            preview_text.insert(tk.END, "Please enter a directory.\n")
            return

        try:
            files_to_rename = get_files_to_rename(rename_directory)
            if not files_to_rename:
                preview_text.insert(tk.END, f"No files found in '{rename_directory}'.\n")
                return

            rename_actions = preview_rename_actions(files_to_rename, operation, prefix, string_to_replace, replacement_string)

            if rename_actions:
                preview_text.insert(tk.END, "--- Preview of Renames ---\n")
                for old_name, new_name in rename_actions:
                    preview_text.insert(tk.END, f"{old_name} -> {new_name}\n")
                preview_text.insert(tk.END, "\n---------------------------\n")
            else:
                preview_text.insert(tk.END, "No files will be renamed based on your criteria.\n")

        except FileNotFoundError:
            preview_text.insert(tk.END, f"Error: Directory '{rename_directory}' not found.\n")
        except Exception as e:
            preview_text.insert(tk.END, f"An error occurred during preview: {e}\n")

    preview_button = ttk.Button(rename_window, text="Preview Rename", command=perform_preview)
    preview_button.grid(row=5, column=0, columnspan=3, pady=5)

    results_frame = ttk.LabelFrame(rename_window, text="Rename Results")
    results_frame.grid(row=6, column=0, columnspan=3, padx=5, pady=5, sticky=tk.NSEW)
    rename_window.grid_rowconfigure(6, weight=1)
    results_text = scrolledtext.ScrolledText(results_frame, height=5, wrap=tk.WORD)
    results_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def perform_rename():
        rename_directory = dir_entry.get()
        operation = operation_var.get()
        prefix = prefix_entry.get()
        string_to_replace = replace_from_entry.get()
        replacement_string = replace_to_entry.get()
        results_text.delete(1.0, tk.END)

        if not rename_directory:
            results_text.insert(tk.END, "Please enter a directory.\n")
            return

        try:
            renamed_count = perform_bulk_rename(rename_directory, operation, prefix, string_to_replace, replacement_string, results_text)
            results_text.insert(tk.END, f"\nSuccessfully renamed {renamed_count} files.\n")
        except FileNotFoundError:
            results_text.insert(tk.END, f"Error: Directory '{rename_directory}' not found.\n")
        except Exception as e:
            results_text.insert(tk.END, f"An error occurred during renaming: {e}\n")

    rename_button = ttk.Button(rename_window, text="Perform Rename", command=perform_rename)
    rename_button.grid(row=7, column=1, padx=5, pady=10)