# desktop_monitor.py

import tkinter as tk
from tkinter import ttk, scrolledtext
import time
import threading
import psutil

monitoring_active = False
monitor_thread = None

def get_system_stats():
    """Retrieves CPU and memory usage."""
    cpu_usage = psutil.cpu_percent()
    memory = psutil.virtual_memory()
    memory_usage_percent = memory.percent
    return cpu_usage, memory_usage_percent

def monitor_desktop(output_widget, stop_event):
    """Monitors CPU and memory usage and updates the output widget."""
    output_widget.insert(tk.END, "Desktop monitoring started...\n")
    output_widget.see(tk.END)
    while not stop_event.is_set():
        cpu, mem = get_system_stats()
        output_widget.insert(tk.END, f"CPU Usage: {cpu}%, Memory Usage: {mem}%\n")
        output_widget.see(tk.END)
        time.sleep(1)
    output_widget.insert(tk.END, "Desktop monitoring stopped.\n")
    output_widget.see(tk.END)
    global monitoring_active
    monitoring_active = False

def start_monitoring(output_widget, start_button, stop_button):
    """Starts the desktop monitoring in a separate thread."""
    global monitoring_active, monitor_thread, stop_event
    if not monitoring_active:
        monitoring_active = True
        stop_event = threading.Event()
        monitor_thread = threading.Thread(target=monitor_desktop, args=(output_widget, stop_event))
        monitor_thread.start()
        start_button.config(state=tk.DISABLED)
        stop_button.config(state=tk.NORMAL)

def stop_monitoring():
    """Stops the desktop monitoring thread."""
    global monitoring_active, stop_event
    if monitoring_active:
        stop_event.set()
        if monitor_thread and monitor_thread.is_alive():
            monitor_thread.join()
        monitoring_active = False

def create_gui(parent):
    monitor_window = tk.Toplevel(parent)
    monitor_window.title("Desktop Monitoring")

    results_frame = ttk.LabelFrame(monitor_window, text="Monitoring Output")
    results_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    output_text = scrolledtext.ScrolledText(results_frame, height=10, wrap=tk.WORD)
    output_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    button_frame = ttk.Frame(monitor_window)
    button_frame.pack(pady=10)

    start_button = ttk.Button(button_frame, text="Start Monitoring", command=lambda: start_monitoring(output_text, start_button, stop_button))
    start_button.pack(side=tk.LEFT, padx=10)

    stop_button = ttk.Button(button_frame, text="Stop Monitoring", command=stop_monitoring, state=tk.DISABLED)
    stop_button.pack(side=tk.LEFT, padx=10)

    monitor_window.protocol("WM_DELETE_WINDOW", stop_monitoring) 
