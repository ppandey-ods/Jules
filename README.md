# Photo Organizer Web App

This is a simple web application built with Flask that allows you to organize your photos by date or location.

## Prerequisites

- Python 3.8 or higher
- `pip` for installing packages

## Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd <repository_name>
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install the dependencies:**
    The project uses `pyproject.toml` to define dependencies. You can install them using `pip`:
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

1.  **Enter the source directory:**
    Provide the absolute path to the directory containing the photos you want to organize. For testing, you can use the `mock_images` directory provided in this project. You will need to provide the full path to it, for example: `/path/to/your/project/mock_images`.

2.  **Enter the destination directory:**
    Provide the absolute path to the directory where you want the organized photos to be stored. This directory will be created if it doesn't exist.

3.  **Choose an organization strategy:**
    -   **Date:** Organizes photos into `YYYY/MM` subfolders.
    -   **Location:** Organizes photos into subfolders named after the location (e.g., `paris`, `london`).

4.  **Select cloud sync options (optional):**
    Check the boxes to simulate syncing the organized photos to Google Drive or OneDrive.

5.  **Click "Organize Photos":**
    The application will process your photos and display a log of the operations on the results page.
