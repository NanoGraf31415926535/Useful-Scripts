import platform
import psutil
import tkinter as tk
from tkinter import ttk, scrolledtext

def get_system_info():
    """Collects and returns system information as a string."""
    info = f"Operating System: {platform.system()} {platform.release()}\n"
    info += f"Architecture: {platform.architecture()[0]}\n"
    info += f"Hostname: {platform.node()}\n"
    info += f"Processor: {platform.processor()}\n\n"

    cpu_percent = psutil.cpu_percent(interval=1)
    info += f"CPU Usage: {cpu_percent}%\n"
    cpu_cores = psutil.cpu_count(logical=True)
    info += f"CPU Cores (Logical): {cpu_cores}\n\n"

    memory = psutil.virtual_memory()
    total_memory_gb = memory.total / (1024 ** 3)
    available_memory_gb = memory.available / (1024 ** 3)
    memory_percent = memory.percent
    info += f"Total Memory: {total_memory_gb:.2f} GB\n"
    info += f"Available Memory: {available_memory_gb:.2f} GB\n"
    info += f"Memory Usage: {memory_percent}%\n\n"

    disk = psutil.disk_usage('/')
    total_disk_gb = disk.total / (1024 ** 3)
    used_disk_gb = disk.used / (1024 ** 3)
    free_disk_gb = disk.free / (1024 ** 3)
    disk_percent = disk.percent
    info += f"Total Disk Space: {total_disk_gb:.2f} GB\n"
    info += f"Used Disk Space: {used_disk_gb:.2f} GB\n"
    info += f"Free Disk Space: {free_disk_gb:.2f} GB\n"
    info += f"Disk Usage: {disk_percent}%\n"

    return info

def create_gui(parent):
    info_window = tk.Toplevel(parent)
    info_window.title("System Information")
    info_text = scrolledtext.ScrolledText(info_window, height=15, width=60, wrap=tk.WORD)
    info_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
    system_info = get_system_info()
    info_text.insert(tk.END, system_info)
    info_text.config(state=tk.DISABLED) 