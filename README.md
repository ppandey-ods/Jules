# Photo Organizer Web App

A simple web application built with Flask that allows you to organize your photos by date or location using their real EXIF data.

## Features

*   **Organize by Date:** Automatically sorts photos into `YYYY/MM` folders based on the date the photo was taken.
*   **Organize by Location:** Sorts photos into folders based on the GPS coordinates found in the EXIF data (e.g., `Lat_48.86_Lon_2.35`).
*   **Easy to Use Interface:** A simple web page with native folder selection dialogs, so you don't have to type out long file paths.
*   **Cloud Sync Simulation:** Includes placeholder functions to show where Google Drive and OneDrive integration would go.

## Prerequisites

*   Python 3.8 or higher
*   `pip` for installing packages

## Installation

1.  **Clone the repository or download the source code.**

2.  **Open your terminal or command prompt** in the project's root directory.

3.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

4.  **Install the dependencies:**
    With the virtual environment active, run the following command to install Flask, ExifRead, and other necessary packages:
    ```bash
    pip install .
    ```

## How to Run

1.  **Run the Flask application:**
    ```bash
    flask run
    ```
    Alternatively, you can run the `app.py` file directly:
    ```bash
    python app.py
    ```

2.  **Open the web interface:**
    Open your web browser and navigate to:
    ```
    http://127.0.0.1:5000
    ```

## How to Use

1.  **Select Source Directory:** Click the "Browse..." button next to "Source Directory" to open a dialog and select the folder containing your photos.
2.  **Select Destination Directory:** Click the "Browse..." button for the destination to select where the organized photos will be stored.
3.  **Choose Strategy:** Select either "Date" or "Location" from the dropdown menu.
4.  **Cloud Sync (Optional):** Check the boxes to simulate syncing to Google Drive or OneDrive.
5.  **Click "Organize Photos":** The application will process your photos and display a log of all operations on the results page.
