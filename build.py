#!/usr/bin/env python3
"""
Build script to create an executable from the Calorie Tracker application
This script uses PyInstaller to create a standalone executable
"""

import subprocess
import sys
import os
from pathlib import Path

def install_requirements():
    """Install required packages"""
    print("Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✓ Requirements installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to install requirements: {e}")
        return False
    return True

def build_executable():
    """Build the executable using PyInstaller"""
    print("Building executable...")
    
    # PyInstaller command
    cmd = [
        "pyinstaller",
        "--onefile",                    # Create a single executable file
        "--windowed",                   # No console window (for GUI apps)
        "--name=CalorieTracker",        # Name of the executable
        "--icon=app.ico",               # Icon (optional, will skip if not found)
        "--add-data=*.py;.",            # Include all Python files
        "main.py"                       # Main script
    ]
    
    # Remove icon option if icon file doesn't exist
    if not os.path.exists("app.ico"):
        cmd.remove("--icon=app.ico")
    
    try:
        subprocess.check_call(cmd)
        print("✓ Executable built successfully")
        print("✓ Executable location: dist/CalorieTracker.exe")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to build executable: {e}")
        return False
    except FileNotFoundError:
        print("✗ PyInstaller not found. Installing PyInstaller...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
            print("✓ PyInstaller installed. Retrying build...")
            subprocess.check_call(cmd)
            print("✓ Executable built successfully")
            return True
        except subprocess.CalledProcessError as e:
            print(f"✗ Failed to install or run PyInstaller: {e}")
            return False

def create_simple_build():
    """Create a simple build without PyInstaller (for development)"""
    print("Creating simple build...")
    
    # Create a batch file for Windows
    if os.name == 'nt':  # Windows
        with open("run_calorie_tracker.bat", "w") as f:
            f.write("@echo off\n")
            f.write("python main.py\n")
            f.write("pause\n")
        print("✓ Created run_calorie_tracker.bat")
    
    # Create a shell script for Unix-like systems
    else:
        with open("run_calorie_tracker.sh", "w") as f:
            f.write("#!/bin/bash\n")
            f.write("python3 main.py\n")
        
        # Make it executable
        os.chmod("run_calorie_tracker.sh", 0o755)
        print("✓ Created run_calorie_tracker.sh")

def main():
    """Main build function"""
    print("=== Calorie Tracker Build Script ===")
    
    # Check if Python files exist
    required_files = ["main.py", "gui.py", "data_manager.py", "visualizer.py"]
    for file in required_files:
        if not os.path.exists(file):
            print(f"✗ Required file missing: {file}")
            return
    
    print("✓ All required files found")
    
    # Ask user for build type
    print("\nBuild options:")
    print("1. Full executable (recommended) - requires PyInstaller")
    print("2. Simple runner script - no additional dependencies")
    print("3. Install requirements only")
    
    try:
        choice = input("\nSelect option (1/2/3): ").strip()
    except KeyboardInterrupt:
        print("\nBuild cancelled.")
        return
    
    if choice == "1":
        # Install requirements first
        if not install_requirements():
            print("Build failed due to requirements installation.")
            return
        
        # Build executable
        if build_executable():
            print("\n🎉 Build completed successfully!")
            print("You can run the application by executing: dist/CalorieTracker.exe")
        else:
            print("\nBuild failed. Creating simple runner instead...")
            create_simple_build()
    
    elif choice == "2":
        install_requirements()
        create_simple_build()
        print("\n✓ Simple build completed!")
        if os.name == 'nt':
            print("Run the application by double-clicking: run_calorie_tracker.bat")
        else:
            print("Run the application by executing: ./run_calorie_tracker.sh")
    
    elif choice == "3":
        install_requirements()
        print("\n✓ Requirements installed!")
        print("Run the application with: python main.py")
    
    else:
        print("Invalid choice. Please run the script again.")

if __name__ == "__main__":
    main()