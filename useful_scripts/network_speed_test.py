import speedtest
import tkinter as tk
from tkinter import ttk, scrolledtext
from speedtest import SpeedtestException
import requests

def run_speed_test(output_widget):
    """Runs the network speed test and updates the output widget."""
    output_widget.delete(1.0, tk.END)
    try:
        st = speedtest.Speedtest()
        output_widget.insert(tk.END, "Finding best server...\n")
        output_widget.update()
        st.get_best_server()
        output_widget.insert(tk.END, "Performing download test...\n")
        output_widget.update()
        download_speed_bps = st.download()
        output_widget.insert(tk.END, "Performing upload test...\n")
        output_widget.update()
        upload_speed_bps = st.upload()

        download_speed_mbps = download_speed_bps / 1_000_000
        upload_speed_mbps = upload_speed_bps / 1_000_000

        output_widget.insert(tk.END, f"Download Speed: {download_speed_mbps:.2f} Mbps\n")
        output_widget.insert(tk.END, f"Upload Speed: {upload_speed_mbps:.2f} Mbps\n")
    except SpeedtestException as e:
        if "HTTP Error 403" in str(e):
            output_widget.insert(tk.END, "Error during speed test: Access to the server was denied (HTTP 403 Forbidden).\n")
            output_widget.insert(tk.END, "This might be a temporary issue with the server or your network.\nPlease try again later.\n")
        else:
            output_widget.insert(tk.END, f"Error during speed test: {e}\n")
    except requests.exceptions.RequestException as e:
        output_widget.insert(tk.END, f"Network error during speed test: {e}\nCheck your internet connection.\n")
    except Exception as e:
        output_widget.insert(tk.END, f"An unexpected error occurred: {e}\n")

def create_gui(parent):
    test_window = tk.Toplevel(parent)
    test_window.title("Network Speed Test")
    results_text = scrolledtext.ScrolledText(test_window, height=5, wrap=tk.WORD)
    results_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    def perform_test():
        run_speed_test(results_text)

    start_button = ttk.Button(test_window, text="Start Speed Test", command=perform_test)
    start_button.pack(pady=5)