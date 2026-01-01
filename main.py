#!/usr/bin/env python3
"""
Calorie Tracker Desktop Application
Main entry point for the application
"""

import tkinter as tk
from tkinter import messagebox
import sys
import os

# Add the current directory to Python path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from gui import CalorieTrackerGUI
except ImportError as e:
    messagebox.showerror("Import Error", f"Failed to import required modules: {str(e)}")
    sys.exit(1)


def main():
    """Main application entry point"""
    try:
        # Create the main window
        root = tk.Tk()
        
        # Create and run the application
        app = CalorieTrackerGUI(root)
        
        # Start the GUI event loop
        root.mainloop()
        
    except Exception as e:
        messagebox.showerror("Application Error", f"An error occurred: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()