# SheetBridge

SheetBridge is a Python utility designed to facilitate the uploading of CSV files to Google Sheets and downloading content from Google Sheets into CSV format. It provides a command-line interface for easy operation.

## Features

- **Upload CSV**: Upload data from a CSV file directly into a specified Google Sheet.
- **Download to CSV**: Download data from a specified Google Sheet into a CSV file.
- **Flexible Targeting**: Specify the starting cell for uploads and downloads.
- **Google Sheets API**: Utilizes Google Sheets API for robust and secure data handling.

## Installation

Before running the script, ensure that you have Python installed on your system and the following Python packages:

```bash
pip install gspread oauth2client pandas
```

## Setup

1. **Google Cloud Platform Project**: You must have a Google Cloud Platform project with the Google Sheets API enabled.
2. **Credentials**: You need to set up credentials:
    - Navigate to the Google Cloud Console.
    - Enable the Google Sheets API.
    - Create credentials for a Desktop application.
    - Download the JSON file containing your credentials.

## Usage

### Upload Data to Google Sheets

To upload data from a CSV file to Google Sheets:

```bash
python sheetbridge.py upload <credentials.json> <yourfile.csv> <google_sheet_url> <sheet_name> <start_cell>
```

### Download Data from Google Sheets

To download data from Google Sheets to a CSV file:

```bash
python sheetbridge.py download <credentials.json> <output.csv> <google_sheet_url> <sheet_name> <start_cell>
```

### Parameters

- `action`: `upload` or `download` depending on the desired operation.
- `credentials.json`: Path to the JSON file containing your Google API credentials.
- `yourfile.csv` or `output.csv`: Path to the CSV file for upload or the destination path for the download.
- `google_sheet_url`: URL of the Google Sheet (make sure you have access rights).
- `sheet_name`: Name of the worksheet in the Google Sheet.
- `start_cell`: Cell in the worksheet where data upload or download begins.

## Security Note

Handle your JSON credentials file securely. Do not expose this file in public repositories or unsecured locations.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
```
