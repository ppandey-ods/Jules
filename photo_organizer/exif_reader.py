import os
import re
from typing import Dict, Any, Optional

# Mock GPS data for locations
LOCATION_COORDINATES = {
    "paris": (48.8566, 2.3522),
    "london": (51.5074, -0.1278),
    "tokyo": (35.6895, 139.6917),
}

def to_dms(decimal_degree):
    """Converts decimal degrees to degrees, minutes, seconds."""
    degrees = int(decimal_degree)
    minutes = int((decimal_degree - degrees) * 60)
    seconds = (decimal_degree - degrees - minutes / 60) * 3600
    return degrees, minutes, seconds

def read_exif_data(image_path: str) -> Optional[Dict[str, Any]]:
    """
    Mocks reading EXIF data from an image file by parsing its filename.
    Filename format is expected to be: {location}_{YYYY}_{MM}_{DD}_{n}.jpg
    """
    filename = os.path.basename(image_path)
    match = re.match(r"(\w+)_(\d{4})_(\d{2})_(\d{2})_?(\d*)\.jpg", filename)

    if not match:
        # Handle the no_location case
        match_no_loc = re.match(r"no_location_(\d{4})_(\d{2})_(\d{2})\.jpg", filename)
        if not match_no_loc:
            return None

        year, month, day = match_no_loc.groups()
        return {
            "DateTimeOriginal": f"{year}:{month}:{day} 12:00:00",
            "GPSInfo": None
        }

    location, year, month, day, _ = match.groups()

    exif_data = {
        "DateTimeOriginal": f"{year}:{month}:{day} 12:00:00",
        "GPSInfo": None
    }

    if location in LOCATION_COORDINATES:
        lat, lon = LOCATION_COORDINATES[location]
        lat_dms = to_dms(abs(lat))
        lon_dms = to_dms(abs(lon))

        exif_data["GPSInfo"] = {
            "GPSLatitudeRef": "N" if lat >= 0 else "S",
            "GPSLatitude": lat_dms,
            "GPSLongitudeRef": "E" if lon >= 0 else "W",
            "GPSLongitude": lon_dms,
        }

    return exif_data
