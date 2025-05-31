
# Bulk Zip Extractor

## Overview

**Bulk Zip Extractor** is a Python application designed to simplify the process of extracting multiple ZIP files at once. With a clean and simple GUI built using **Tkinter**, users can easily select source and destination directories and track the progress of their extraction tasks. This app also supports nested ZIP files, extracting them recursively as needed.

## Key Features

- **User-friendly GUI**: Built with Tkinter, making it easy to select the source and destination folders.
- **Bulk ZIP Extraction**: Supports extracting multiple ZIP files from the source folder in one go.
- **Nested ZIP Handling**: Automatically detects ZIP files within ZIP files and extracts them recursively.
- **Progress Bar**: Displays real-time progress of the extraction process.
- **Countdown Timer**: Provides an estimated time remaining for the entire extraction.
- **Background Processing**: Extraction happens in a background thread, ensuring the GUI remains responsive.
- **Error Handling**: The application continues processing other files if an error occurs with any ZIP file.

## Installation

To run the application, you will need **Python** installed on your system.

### Step 1: Install Python

Ensure that Python 3.6 or higher is installed on your machine. You can download Python from the official website:

[Download Python](https://www.python.org/downloads/)

### Step 2: Install Required Libraries

This application requires the **Tkinter** library for the GUI. It’s typically included with Python, but if it’s missing, you can install it via pip:

```bash
pip install tk
```

### Step 3: Download or Clone the Repository

You can download or clone the repository to your local machine. To clone:

```bash
git clone https://github.com/ghedgebeth/bulk-unzip
```

### Step 4: Run the Application

Navigate to the folder containing the application and run:

```bash
python bulkUnzipper1-6.py
```

## Usage

### 1. Select the Source Folder
Click on the **"Select Source Folder"** button to choose the folder that contains the ZIP files you want to extract.

### 2. Select the Destination Folder
Click on the **"Select Destination Folder"** button to choose the folder where the extracted files will be saved.

### 3. Start Extraction
Click on the **"Extract ZIP Files"** button to start extracting. The app will:
- Extract all ZIP files in the source folder.
- Automatically handle any nested ZIP files within the extracted files.
- Show the extraction progress in the progress bar.

### 4. Progress Bar and Countdown Timer
- **Progress Bar**: Displays how much of the extraction is completed.
- **Countdown Timer**: Displays an estimate of how much time is remaining for the process to complete.

### 5. Error Handling
If an error occurs with any ZIP file (e.g., the file is corrupted), the app will skip that file and continue extracting the rest.

## Code Overview

The code is organized into the following key sections:

1. **GUI Initialization**: Sets up the main Tkinter window and the user interface components (buttons, progress bar, and countdown).
2. **Folder Selection**: Allows users to select both source and destination folders via file dialogs.
3. **Extraction Logic**: Extracts ZIP files and recursively handles nested ZIP files. Extraction runs in a separate thread to ensure the GUI stays responsive.
4. **Progress Tracking**: The progress bar and countdown timer are updated in the main thread based on the current extraction progress.
5. **Error Handling**: The app continues processing other ZIP files even if there’s an error with one.

## Contributing

If you'd like to contribute to this project, feel free to fork the repository, make changes, and submit a pull request.


## License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## Screenshots

![Bulk Zip Extractor](https://github.com/user-attachments/assets/34d4dd18-c77f-4532-b4a2-f432cc4ae927)

*Example screenshot showing the Bulk Zip Extractor GUI in action.*

---

### Enjoy the convenience of batch extracting ZIP files with ease!

