# Useful Scripts GUI

This project is a collection of helpful Python scripts wrapped in a user-friendly graphical interface built with Tkinter. The goal is to provide easy access to various system and file management utilities for users who may not be comfortable with command-line interfaces.

## Overview

The application presents a main window with a list of available scripts. Each script can be launched by clicking its corresponding button, which will open a new window with the specific controls and output area for that tool.

The following tools are currently included:

1.  **Desktop Monitoring:** Monitors and displays real-time CPU and memory usage.
2.  **File Search:** Allows you to search for files by name (or part of the name) within a specified directory.
3.  **Duplicate File Finder:** Finds and lists duplicate files within a given directory based on file content.
4.  **Bulk Rename Tool:** Provides options to rename multiple files in a directory by adding a prefix or replacing a specific string.
5.  **File Type Counter:** Scans a directory and counts the number of files for each file extension.
6.  **Create Empty Files/Folders:** Enables the creation of multiple empty files or folders in a specified directory.
7.  **System Info Display:** Shows basic information about your operating system, processor, memory, and disk usage.
8.  **Network Speed Test:** Performs a quick test of your internet download and upload speeds.
9.  **Clipboard History:** Monitors and displays a history of items copied to your clipboard.
10. **Clear Temporary Files:** Attempts to clear temporary files and folders from your system's temporary directory.
11. **Clear Python Package Cache (pip):** Provides an option to clear the Python package installer (pip) cache.

## Getting Started

### Prerequisites

* **Python 3:** This project is written in Python 3. Ensure you have it installed on your system.
* **Required Libraries:** Some scripts depend on external libraries. You can install them using pip:
    ```bash
    pip install psutil speedtest-cli pyperclip
    ```

### Installation

1.  **Clone the repository** (if you have the code in a repository) or **download the files** to a directory on your computer.
2.  **Navigate to the project directory** in your terminal.

### Running the Application

1.  Execute the `main.py` script:
    ```bash
    python main.py
    ```
2.  This will open the main "Useful Scripts" window. Click on the buttons to open and use the individual tools.

## Usage

Each tool has its own dedicated window with specific instructions and input fields. Generally, you will:

1.  Click the button for the desired tool in the main window.
2.  A new window will appear with controls relevant to that tool.
3.  Enter the required information (e.g., directory paths, search queries, rename options).
4.  Click the appropriate button (e.g., "Search", "Find Duplicates", "Perform Rename") to execute the script.
5.  The results or output will be displayed in the window, usually in a text area.

For tools that involve file system modifications (like Bulk Rename and Clear Temporary Files), be cautious and review any previews or confirmations before proceeding.

## Project Structure

```
UsefulScriptsGUI/
├── useful_scripts/
│   ├── __init__.py
│   ├── bulk_rename.py
│   ├── clear_pip_cache.py
│   ├── clear_temp.py
│   ├── clipboard_history.py
│   ├── create_empty.py
│   ├── desktop_monitor.py
│   ├── duplicate_finder.py
│   ├── file_search.py
│   ├── file_type_counter.py
│   └── system_info.py
├── main.py
└── README.md
```

* `main.py`: The main script that creates the GUI application and houses the main window.
* `useful_scripts/`: A directory containing the individual Python scripts for each tool. Each script now manages its own `Toplevel` window and logic.
* `README.md`: This file, providing information about the project.

## Contributing

Contributions to this project are welcome. If you have ideas for new useful scripts or improvements to existing ones, feel free to:

1.  Fork the repository.
2.  Create a new branch for your changes.
3.  Implement your changes and test them thoroughly.
4.  Submit a pull request.

Please ensure your code follows good Python practices and includes clear comments.

## License

This project is open-source.