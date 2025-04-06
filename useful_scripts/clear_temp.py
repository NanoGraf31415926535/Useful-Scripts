import os
import shutil
import tempfile
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox

def clear_temp_files_gui(output_widget):
    """Clears temporary files and updates the output widget."""
    temp_dir = tempfile.gettempdir()
    cleared_count = 0
    errors = []
    output_widget.insert(tk.END, f"Attempting to clear temporary files in: {temp_dir}\n")

    for item in os.listdir(temp_dir):
        item_path = os.path.join(temp_dir, item)
        try:
            if os.path.isfile(item_path):
                os.remove(item_path)
                cleared_count += 1
                output_widget.insert(tk.END, f"Deleted file: {item_path}\n")
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)
                cleared_count += 1
                output_widget.insert(tk.END, f"Deleted folder: {item_path}\n")
        except OSError as e:
            error_message = f"Error deleting '{item}': {e}\n"
            errors.append(error_message)
            output_widget.insert(tk.END, error_message)
        except Exception as e:
            error_message = f"An unexpected error occurred while trying to delete '{item}': {e}\n"
            errors.append(error_message)
            output_widget.insert(tk.END, error_message)

    return cleared_count, errors

def create_gui(parent):
    clear_window = tk.Toplevel(parent)
    clear_window.title("Clear Temporary Files")
    results_text = scrolledtext.ScrolledText(clear_window, height=8, wrap=tk.WORD)
    results_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    def perform_clear():
        results_text.delete(1.0, tk.END)
        confirm = messagebox.askyesno("Confirm Clear", "Are you sure you want to clear temporary files?", parent=clear_window)
        if confirm:
            cleared_count, errors = clear_temp_files_gui(results_text)
            results_text.insert(tk.END, f"\nSuccessfully deleted {cleared_count} temporary files/folders (attempted).\n")
            if errors:
                results_text.insert(tk.END, "\n--- Errors Encountered ---\n")
                for error in errors:
                    results_text.insert(tk.END, f"{error}\n")
                results_text.insert(tk.END, "Note: Some files/folders might be in use and could not be deleted.\n")
            else:
                results_text.insert(tk.END, "No errors encountered during deletion.\n")
        else:
            results_text.insert(tk.END, "Temporary file clearing cancelled.\n")

    clear_button = ttk.Button(clear_window, text="Clear Temporary Files", command=perform_clear)
    clear_button.pack(pady=10)