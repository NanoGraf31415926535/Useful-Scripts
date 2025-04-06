import tkinter as tk
from tkinter import ttk, scrolledtext
import pyperclip

clipboard_history = []

def update_history(history_text):
    """Updates the clipboard history displayed in the text widget."""
    global clipboard_history
    try:
        current_clipboard = pyperclip.paste()
        if current_clipboard and (not clipboard_history or clipboard_history[-1] != current_clipboard):
            clipboard_history.append(current_clipboard)
            # Keep only the last 10 items for brevity
            clipboard_history = clipboard_history[-10:]
            history_text.delete(1.0, tk.END)
            history_text.insert(tk.END, "\n".join(clipboard_history[::-1])) # Show newest at the top
    except pyperclip.PyperclipException as e:
        history_text.delete(1.0, tk.END)
        history_text.insert(tk.END, f"Error accessing clipboard: {e}\nMake sure you have a copy/paste mechanism installed (e.g., xclip on Linux).\n")
    except Exception as e:
        history_text.delete(1.0, tk.END)
        history_text.insert(tk.END, f"An unexpected error occurred: {e}\n")
    history_text.after(1000, lambda: update_history(history_text)) # Update every 1 second

def create_gui(parent):
    history_window = tk.Toplevel(parent)
    history_window.title("Clipboard History")
    history_text = scrolledtext.ScrolledText(history_window, height=10, width=60, wrap=tk.WORD)
    history_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    # Initial update and start the recurring update
    update_history(history_text)

# The if __name__ == "__main__": block is no longer needed here