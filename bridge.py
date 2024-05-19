import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import argparse
import sys


def authenticate_gspread(json_creds):
    scope = ['https://www.googleapis.com/auth/spreadsheets']
    creds = ServiceAccountCredentials.from_json_keyfile_name(json_creds, scope)
    client = gspread.authorize(creds)
    return client


def upload_to_sheet(json_creds, file_path, url, sheet_name, start_cell, erase):
    client = authenticate_gspread(json_creds)
    sheet = client.open_by_url(url)

    try:
        worksheet = sheet.worksheet(sheet_name)
        if erase:
            worksheet.clear()
            print(f"Worksheet '{sheet_name}' cleared.")
    except gspread.exceptions.WorksheetNotFound:
        print(f"Worksheet '{sheet_name}' not found. Creating a new worksheet.")
        worksheet = sheet.add_worksheet(title=sheet_name, rows="1000", cols="26")

    data = pd.read_csv(file_path)
    data = data.fillna('')  # JSON can't handle nan values, so we need to filter them out here
    cell_list = worksheet.range(
        start_cell + ':' + gspread.utils.rowcol_to_a1(data.shape[0] + worksheet.range(start_cell)[0].row - 1,
                                                      data.shape[1] + worksheet.range(start_cell)[0].col - 1))

    # Pandas doesn't consider the header to be part of the data, but we also want to write it back
    # so we manually add them both together
    flat_list = data.columns.tolist() + data.values.ravel().tolist()

    for cell, value in zip(cell_list, flat_list):
        cell.value = value
    worksheet.update_cells(cell_list)


def download_from_sheet(json_creds, url, sheet_name, start_cell, output_file):
    client = authenticate_gspread(json_creds)
    sheet = client.open_by_url(url)
    worksheet = sheet.worksheet(sheet_name)
    data = worksheet.get(start_cell + ':' + gspread.utils.rowcol_to_a1(worksheet.row_count,
                                                                       worksheet.col_count))
    df = pd.DataFrame(data)
    df.to_csv(output_file, index=False, header=False)


def main():
    parser = argparse.ArgumentParser(description='Upload or download a CSV to/from Google Sheets.')
    parser.add_argument('action', choices=['upload', 'download'], help='Action to perform: upload or download')
    parser.add_argument('json_creds', help='Path to JSON credentials file')
    parser.add_argument('file_path', help='Path to the CSV file for upload or destination for download')
    parser.add_argument('url', help='URL of the Google Sheet')
    parser.add_argument('sheet_name', help='Name of the worksheet in the Google Sheet')
    parser.add_argument('start_cell', help='Start cell for upload or download')
    parser.add_argument('--erase', action='store_true', help='Erase the worksheet before uploading')
    args = parser.parse_args()

    if args.action == 'upload':
        upload_to_sheet(args.json_creds, args.file_path, args.url, args.sheet_name, args.start_cell, args.erase)
    elif args.action == 'download':
        download_from_sheet(args.json_creds, args.url, args.sheet_name, args.start_cell, args.file_path)


if __name__ == "__main__":
    main()