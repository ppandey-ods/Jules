import os
import re
import shutil
from datetime import datetime
from typing import List
from .image_discovery import discover_images
from .exif_reader import read_exif_data, LOCATION_COORDINATES

# Reverse mapping from coordinates to location name
COORDINATES_TO_LOCATION = {v: k for k, v in LOCATION_COORDINATES.items()}

def organize_photos(source_dir: str, dest_dir: str, strategy: str):
    """
    Organizes photos from a source directory into a destination directory.

    Args:
        source_dir: The directory containing the images to organize.
        dest_dir: The root directory where organized folders will be created.
        strategy: The organization strategy, either 'date' or 'location'.
    """
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    images = discover_images(source_dir)
    logs = []

    for image_path in images:
        exif_data = read_exif_data(image_path)
        if not exif_data:
            logs.append(f"Warning: Could not read EXIF data for {image_path}. Skipping.")
            continue

        target_subfolder = ""
        if strategy == "date":
            try:
                date_str = exif_data["DateTimeOriginal"]
                dt_object = datetime.strptime(date_str, "%Y:%m:%d %H:%M:%S")
                target_subfolder = os.path.join(str(dt_object.year), f"{dt_object.month:02d}")
            except (KeyError, ValueError):
                logs.append(f"Warning: Could not find or parse date for {image_path}. Skipping.")
                continue

        elif strategy == "location":
            gps_info = exif_data.get("GPSInfo")
            if not gps_info:
                logs.append(f"Warning: No GPS info for {image_path}. Skipping.")
                continue

            filename = os.path.basename(image_path)
            match = re.match(r"^([a-zA-Z]+)_", filename)
            if match:
                location_name = match.group(1)
                if location_name != "no": # to exclude no_location
                    target_subfolder = location_name
                else:
                    logs.append(f"Warning: Could not determine location for {image_path}. Skipping.")
                    continue
            else:
                logs.append(f"Warning: Could not determine location for {image_path}. Skipping.")
                continue

        else:
            logs.append(f"Error: Unknown strategy '{strategy}'.")
            return logs

        if target_subfolder:
            final_dest_dir = os.path.join(dest_dir, target_subfolder)
            if not os.path.exists(final_dest_dir):
                os.makedirs(final_dest_dir)

            shutil.move(image_path, os.path.join(final_dest_dir, os.path.basename(image_path)))
            logs.append(f"Moved {image_path} to {final_dest_dir}")

    return logs
