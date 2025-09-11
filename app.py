from flask import Flask, render_template, request, jsonify
from photo_organizer.organizer import organize_photos
from photo_organizer.cloud_sync import sync_to_google_drive, sync_to_one_drive
import os
import shutil
import tkinter as tk
from tkinter import filedialog

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/select-folder')
def select_folder():
    """Opens a native folder selection dialog."""
    root = tk.Tk()
    root.withdraw()  # Hide the main tkinter window
    folder_path = filedialog.askdirectory(master=root)
    root.destroy()
    return jsonify({'path': folder_path})

@app.route('/organize', methods=['POST'])
def organize():
    source_dir = request.form.get('source_dir')
    dest_dir = request.form.get('dest_dir')
    strategy = request.form.get('strategy')
    sync_google = request.form.get('sync_google_drive')
    sync_onedrive = request.form.get('sync_one_drive')

    all_logs = []

    # Basic validation
    if not source_dir or not dest_dir:
        all_logs.append("Error: Source and destination directories are required.")
        return render_template('results.html', logs=all_logs)

    # For safety and to avoid modifying original files, we'll work on a copy
    # In a real app, you might want a different strategy
    temp_source = os.path.join(dest_dir, "temp_source_for_web")
    if os.path.exists(temp_source):
        shutil.rmtree(temp_source)

    try:
        shutil.copytree(source_dir, temp_source)
    except FileNotFoundError:
        all_logs.append(f"Error: Source directory '{source_dir}' not found.")
        return render_template('results.html', logs=all_logs)


    organization_logs = organize_photos(temp_source, dest_dir, strategy)
    all_logs.extend(organization_logs)

    if sync_google:
        google_logs = sync_to_google_drive(dest_dir)
        all_logs.extend(google_logs)

    if sync_onedrive:
        onedrive_logs = sync_to_one_drive(dest_dir)
        all_logs.extend(onedrive_logs)

    # Clean up the temporary directory
    shutil.rmtree(temp_source)

    return render_template('results.html', logs=all_logs)

if __name__ == '__main__':
    app.run(debug=True)
