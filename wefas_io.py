import tkinter as tk
from tkinter import filedialog

def wefas_outbound():
    """Get the outbound file name from user"""
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    file_path = filedialog.asksaveasfilename(
        defaultextension=".CSV",  # Default file extension
        filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]  # File types to display
        )
    return file_path

def wefas_inbound():
    """get the inbound file name from user"""
    file_path = filedialog.askopenfilename(
        initialdir="/",
        title="Select a File",
        filetypes=(("Text files", "*.txt"), ("All files", "*.*"))
    )
    return file_path
