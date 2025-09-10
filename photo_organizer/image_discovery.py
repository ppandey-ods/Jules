import os
from typing import List

def discover_images(directory: str) -> List[str]:
    """
    Scans a directory for image files.

    Args:
        directory: The path to the directory to scan.

    Returns:
        A list of paths to image files found in the directory.
    """
    image_files = []
    supported_extensions = {".jpg", ".jpeg", ".png"}
    for root, _, files in os.walk(directory):
        for file in files:
            if os.path.splitext(file)[1].lower() in supported_extensions:
                image_files.append(os.path.join(root, file))
    return image_files
