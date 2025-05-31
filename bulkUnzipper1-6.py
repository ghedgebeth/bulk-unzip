import os
import zipfile
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.ttk import Progressbar
from threading import Thread  # Importing the threading module to run extraction in the background
from multiprocessing import Manager  # For managing shared progress data between threads
import time


class ZipExtractorApp:
    def __init__(self, root):
        """
        Initializes the main application.
        - root: Tkinter's root window, which contains the GUI.
        """
        self.root = root
        self.root.title("Bulk Zip Extractor")  # Set the window title
        self.root.geometry("400x250")  # Set the window size
        
        # Directory paths
        self.source_dir = None  # Will hold the source directory of ZIP files
        self.dest_dir = None  # Will hold the destination directory to extract files to

        # Manager to share progress between threads
        self.progress_data = Manager().dict()  # Create a shared dictionary to track progress
        self.progress_data["current"] = 0  # Initialize progress to 0

        # Setup UI components (buttons, labels, etc.)
        self.create_widgets()

    def create_widgets(self):
        """
        Creates and packs the necessary widgets for the GUI.
        """
        # Button to select the source folder (where the zip files are)
        self.source_button = tk.Button(self.root, text="Select Source Folder", command=self.select_source_folder)
        self.source_button.pack(pady=10)

        # Button to select the destination folder (where the files will be extracted)
        self.dest_button = tk.Button(self.root, text="Select Destination Folder", command=self.select_dest_folder)
        self.dest_button.pack(pady=10)

        # Button to start the extraction process
        self.extract_button = tk.Button(self.root, text="Extract ZIP Files", command=self.start_extraction)
        self.extract_button.pack(pady=10)

        # Label for progress indication
        self.progress_label = tk.Label(self.root, text="Progress:")
        self.progress_label.pack(pady=5)

        # Progress bar for displaying extraction progress
        self.progress = Progressbar(self.root, length=300, mode='determinate')
        self.progress.pack(pady=5)

        # Label for countdown timer to show remaining time
        self.countdown_label = tk.Label(self.root, text="Time Remaining: 00:00")
        self.countdown_label.pack(pady=5)

    def select_source_folder(self):
        """
        Opens a dialog for the user to select the folder containing the zip files.
        Sets the selected directory to self.source_dir.
        """
        self.source_dir = filedialog.askdirectory(title="Select Folder Containing ZIP Files")
        if self.source_dir:
            print(f"Selected Source Folder: {self.source_dir}")

    def select_dest_folder(self):
        """
        Opens a dialog for the user to select the folder where files will be extracted.
        Sets the selected directory to self.dest_dir.
        """
        self.dest_dir = filedialog.askdirectory(title="Select Destination Folder")
        if self.dest_dir:
            print(f"Selected Destination Folder: {self.dest_dir}")

    def extract_zip(self, zip_path, extract_to):
        """
        Extracts a given zip file to the specified directory.
        If the zip file contains nested zip files, those will also be extracted recursively.

        :param zip_path: Path to the zip file to be extracted
        :param extract_to: Directory where the zip file contents will be extracted
        """
        try:
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(extract_to)  # Extract all contents of the zip file
                self.extract_nested_zips(zip_ref, extract_to)  # Recursively extract nested zips if present
        except Exception as e:
            print(f"Error extracting {zip_path}: {e}")
            return False  # Return False if extraction fails
        return True  # Return True if extraction is successful

    def extract_nested_zips(self, zip_ref, extract_to):
        """
        Recursively checks if there are zip files inside the extracted content.
        If any nested zip files are found, they are extracted as well.

        :param zip_ref: The ZipFile object to inspect for nested zip files
        :param extract_to: Directory where the nested zips will be extracted
        """
        for file_name in zip_ref.namelist():
            if file_name.endswith('.zip'):  # Check if the file is a zip file
                nested_zip_path = os.path.join(extract_to, file_name)
                print(f"Found nested zip: {file_name}")
                with open(nested_zip_path, 'wb') as f_out:
                    f_out.write(zip_ref.read(file_name))  # Write the nested zip file to disk
                self.extract_zip(nested_zip_path, extract_to)  # Recursively extract the nested zip
                os.remove(nested_zip_path)  # Clean up the nested zip file after extraction

    def start_extraction(self):
        """
        Starts the extraction process after validating the directories.
        This method also runs extraction in the background using threads.
        """
        if not self.source_dir or not self.dest_dir:
            messagebox.showwarning("Warning", "Please select both source and destination folders.")
            return

        # Get all zip files from the selected source directory
        zip_files = [f for f in os.listdir(self.source_dir) if f.endswith('.zip')]
        total_files = len(zip_files)  # Total number of zip files to process

        if total_files == 0:
            messagebox.showwarning("Warning", "No ZIP files found in the source folder.")
            return

        self.progress["maximum"] = total_files  # Set the maximum value for the progress bar
        self.progress["value"] = 0  # Initialize the progress bar to 0

        # Countdown Timer and Progress Bar Update in the Main Thread
        def update_progress_bar():
            """
            Periodically updates the progress bar based on the current progress.
            """
            try:
                completed = self.progress_data["current"]  # Get the current progress from shared data
                self.progress["value"] = completed  # Update the progress bar
                remaining_time = (total_files - completed) * 3  # Estimate remaining time (approx 3 secs per zip)
                self.update_countdown(remaining_time)  # Update the countdown timer
                self.root.after(100, update_progress_bar)  # Keep updating every 100 ms
            except Exception as e:
                pass  # If no progress yet, just wait

        # Use threading to run the extraction process in the background
        def extract_files():
            """
            Iterates over each zip file and performs extraction.
            """
            for idx, zip_file in enumerate(zip_files):
                zip_path = os.path.join(self.source_dir, zip_file)  # Get the full path of the zip file
                self.extract_zip(zip_path, self.dest_dir)  # Extract the zip file to the destination folder
                self.progress_data["current"] = idx + 1  # Update progress in the shared dictionary

        # Start extraction in a background thread
        self.root.after(0, update_progress_bar)  # Start the progress update loop
        Thread(target=extract_files).start()  # Run extraction in a separate thread

    def update_countdown(self, remaining_time):
        """
        Updates the countdown label based on the remaining extraction time.
        """
        minutes, seconds = divmod(remaining_time, 60)  # Convert seconds to minutes and seconds
        self.countdown_label.config(text=f"Time Remaining: {minutes:02}:{seconds:02}")  # Update label text
        self.countdown_label.update()  # Refresh the label


if __name__ == "__main__":
    root = tk.Tk()  # Create the main window
    app = ZipExtractorApp(root)  # Create the application instance
    root.mainloop()  # Run the Tkinter main loop
