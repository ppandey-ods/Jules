import exifread
from typing import Dict, Any, Optional

def _dms_to_decimal(dms, ref):
    """Converts DMS (degrees, minutes, seconds) from exifread to decimal degrees."""
    degrees = dms[0].num / dms[0].den
    minutes = dms[1].num / dms[1].den / 60.0
    seconds = dms[2].num / dms[2].den / 3600.0

    decimal = degrees + minutes + seconds
    if ref.values in ['S', 'W']:
        decimal = -decimal
    return decimal

def read_exif_data(image_path: str) -> Optional[Dict[str, Any]]:
    """
    Reads EXIF data from an image file using the exifread library.

    Returns a dictionary containing the date and GPS coordinates if available.
    """
    try:
        with open(image_path, 'rb') as f:
            tags = exifread.process_file(f, details=False)
    except Exception:
        # Handle cases where the file cannot be opened or is not an image
        return None

    if not tags:
        return None

    final_data = {
        "DateTimeOriginal": None,
        "GPSInfo": None
    }

    # Extract Date
    date_tag = tags.get('EXIF DateTimeOriginal')
    if date_tag:
        final_data['DateTimeOriginal'] = str(date_tag.values)

    # Extract and process GPS Info
    lat_tag = tags.get('GPS GPSLatitude')
    lat_ref_tag = tags.get('GPS GPSLatitudeRef')
    lon_tag = tags.get('GPS GPSLongitude')
    lon_ref_tag = tags.get('GPS GPSLongitudeRef')

    if lat_tag and lat_ref_tag and lon_tag and lon_ref_tag:
        try:
            latitude = _dms_to_decimal(lat_tag.values, lat_ref_tag)
            longitude = _dms_to_decimal(lon_tag.values, lon_ref_tag)
            final_data['GPSInfo'] = {
                'Latitude': latitude,
                'Longitude': longitude
            }
        except Exception:
            # GPS data might be malformed
            pass

    if final_data['DateTimeOriginal'] or final_data['GPSInfo']:
        return final_data

    return None
