from flask import Flask, request, jsonify, send_from_directory
from photo_organizer.organizer import organize_photos
from photo_organizer.cloud_sync import sync_to_google_drive, sync_to_one_drive
import os
import shutil
import uuid

app = Flask(__name__, static_folder='webapp')

@app.route('/')
def index():
    return send_from_directory('webapp', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('webapp', path)

@app.route('/organize', methods=['POST'])
def organize():
    strategy = request.form.get('strategy')
    sync_google = request.form.get('sync_google_drive')
    sync_onedrive = request.form.get('sync_one_drive')

    # Create a unique temporary directory for this request
    temp_source = os.path.join("temp", str(uuid.uuid4()))
    os.makedirs(temp_source, exist_ok=True)

    dest_dir = os.path.join("organized_photos", str(uuid.uuid4()))
    os.makedirs(dest_dir, exist_ok=True)

    all_logs = []

    if 'files[]' not in request.files:
        return jsonify({'error': 'No files part in the request'}), 400

    files = request.files.getlist('files[]')

    if not files or all(f.filename == '' for f in files):
        return jsonify({'error': 'No selected files'}), 400

    for file in files:
        if file:
            filename = file.filename
            file.save(os.path.join(temp_source, filename))
            all_logs.append(f"Uploaded {filename}")

    organization_logs = organize_photos(temp_source, dest_dir, strategy)
    all_logs.extend(organization_logs)

    if sync_google:
        google_logs = sync_to_google_drive(dest_dir)
        all_logs.extend(google_logs)

    if sync_onedrive:
        onedrive_logs = sync_to_one_drive(dest_dir)
        all_logs.extend(onedrive_logs)

    # Clean up the temporary directories
    shutil.rmtree(temp_source)
    # We might want to keep the destination directory for the user to download
    # For now, let's just log its location
    all_logs.append(f"Organized photos are in {dest_dir}")


    return jsonify({'logs': all_logs})

if __name__ == '__main__':
    app.run(debug=False)
