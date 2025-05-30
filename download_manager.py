import os
import shutil
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox
import requests
import json
import sys
import subprocess

# Version information
VERSION = "1.0.0"
UPDATE_URL = "https://raw.githubusercontent.com/yourusername/download-organizer/main/version.json"  # You'll need to replace this with your actual update URL

def check_for_updates():
    try:
        response = requests.get(UPDATE_URL)
        if response.status_code == 200:
            update_info = response.json()
            if update_info['version'] > VERSION:
                if messagebox.askyesno("Update Available", 
                    f"Version {update_info['version']} is available!\n\n"
                    f"Current version: {VERSION}\n"
                    f"New version: {update_info['version']}\n\n"
                    f"Would you like to update now?"):
                    # Download and run the new version
                    download_update(update_info['download_url'])
                    return True
    except Exception as e:
        print(f"Error checking for updates: {e}")
    return False

def download_update(download_url):
    try:
        # Download the new version
        response = requests.get(download_url)
        if response.status_code == 200:
            # Save the new version
            update_path = os.path.join(os.path.dirname(sys.executable), "Download Organizer_new.exe")
            with open(update_path, 'wb') as f:
                f.write(response.content)
            
            # Create a batch file to handle the update
            batch_path = os.path.join(os.path.dirname(sys.executable), "update.bat")
            with open(batch_path, 'w') as f:
                f.write(f'''@echo off
timeout /t 2 /nobreak
del "{sys.executable}"
move "{update_path}" "{sys.executable}"
start "" "{sys.executable}"
del "%~f0"
''')
            
            # Run the batch file and exit
            subprocess.Popen([batch_path], shell=True)
            sys.exit()
    except Exception as e:
        messagebox.showerror("Update Error", f"Failed to download update: {e}")

# File type mapping
FILE_TYPES = {
    "Images": [".png", ".jpg", ".jpeg", ".gif", ".bmp", ".svg"],
    "PDFs": [".pdf"],
    "Documents": [".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".txt"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Executables": [".exe", ".msi", ".bat", ".sh"],
}

def organize_folder(folder_path):
    if not os.path.exists(folder_path):
        messagebox.showerror("Error", "Selected folder doesn't exist.")
        return

    files = os.listdir(folder_path)
    moved_files = 0

    for file in files:
        file_path = os.path.join(folder_path, file)
        if os.path.isfile(file_path):
            ext = os.path.splitext(file)[1].lower()
            moved = False

            for folder, extensions in FILE_TYPES.items():
                if ext in extensions:
                    target_folder = os.path.join(folder_path, folder)
                    # Only create folder if it doesn't exist
                    if not os.path.exists(target_folder):
                        os.makedirs(target_folder)
                    
                    # Check if file already exists in target folder
                    target_file_path = os.path.join(target_folder, file)
                    if os.path.exists(target_file_path):
                        # Add a number to the filename if it already exists
                        base_name, file_ext = os.path.splitext(file)
                        counter = 1
                        while os.path.exists(target_file_path):
                            new_name = f"{base_name}_{counter}{file_ext}"
                            target_file_path = os.path.join(target_folder, new_name)
                            counter += 1
                    
                    shutil.move(file_path, target_file_path)
                    moved = True
                    moved_files += 1
                    break

            if not moved:
                other_folder = os.path.join(folder_path, "Others")
                # Only create Others folder if it doesn't exist
                if not os.path.exists(other_folder):
                    os.makedirs(other_folder)
                
                # Check if file already exists in Others folder
                target_file_path = os.path.join(other_folder, file)
                if os.path.exists(target_file_path):
                    # Add a number to the filename if it already exists
                    base_name, file_ext = os.path.splitext(file)
                    counter = 1
                    while os.path.exists(target_file_path):
                        new_name = f"{base_name}_{counter}{file_ext}"
                        target_file_path = os.path.join(other_folder, new_name)
                        counter += 1
                
                shutil.move(file_path, target_file_path)
                moved_files += 1

    messagebox.showinfo("Done", f"Organized {moved_files} files!")

# GUI
def run_app():
    def choose_folder():
        path = filedialog.askdirectory()
        if path:
            folder_var.set(path)

    def organize_action():
        organize_folder(folder_var.get())

    def check_updates():
        check_for_updates()

    root = tk.Tk()
    root.title(f"Download Organizer v{VERSION}")
    root.geometry("400x250")
    root.resizable(False, False)

    folder_var = tk.StringVar(value=str(Path.home() / "Downloads"))

    tk.Label(root, text="Folder to Organize:", font=("Arial", 12)).pack(pady=10)
    tk.Entry(root, textvariable=folder_var, width=40).pack(pady=5)
    tk.Button(root, text="Browse", command=choose_folder).pack(pady=5)
    tk.Button(root, text="Organize Now", bg="#4CAF50", fg="white", font=("Arial", 12), command=organize_action).pack(pady=10)
    tk.Button(root, text="Check for Updates", command=check_updates).pack(pady=5)

    # Check for updates on startup
    root.after(1000, check_updates)

    root.mainloop()

if __name__ == "__main__":
    run_app()
