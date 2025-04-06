import subprocess
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox

def clear_pip_cache_gui(output_widget):
    """Clears the pip cache and updates the output widget."""
    output_widget.delete(1.0, tk.END)
    confirm = messagebox.askyesno("Confirm Clear", "Are you sure you want to clear the pip package cache?", parent=output_widget.master.master) # Go up to the Toplevel
    if confirm:
        output_widget.insert(tk.END, "Attempting to clear pip cache...\n")
        try:
            process = subprocess.run(['pip', 'cache', 'purge', '--all'], capture_output=True, text=True, check=True)
            output_widget.insert(tk.END, "Pip cache cleared successfully.\n")
            if process.stdout:
                output_widget.insert(tk.END, "--- Output ---\n")
                output_widget.insert(tk.END, process.stdout)
                output_widget.insert(tk.END, "---------------\n")
            if process.stderr:
                output_widget.insert(tk.END, "--- Errors ---\n")
                output_widget.insert(tk.END, process.stderr)
                output_widget.insert(tk.END, "---------------\n")
        except subprocess.CalledProcessError as e:
            output_widget.insert(tk.END, f"Error clearing pip cache:\n{e}\n")
            if e.stderr:
                output_widget.insert(tk.END, f"--- Error Output ---\n{e.stderr}\n--------------------\n")
        except FileNotFoundError:
            output_widget.insert(tk.END, "Error: 'pip' command not found. Make sure pip is installed and in your system's PATH.\n")
        except Exception as e:
            output_widget.insert(tk.END, f"An unexpected error occurred: {e}\n")
    else:
        output_widget.insert(tk.END, "Pip cache clearing cancelled.\n")

def create_gui(parent):
    clear_window = tk.Toplevel(parent)
    clear_window.title("Clear Python Package Cache (pip)")
    results_text = scrolledtext.ScrolledText(clear_window, height=5, wrap=tk.WORD)
    results_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    def perform_clear():
        clear_pip_cache_gui(results_text)

    clear_button = ttk.Button(clear_window, text="Clear Pip Cache", command=perform_clear)
    clear_button.pack(pady=10)