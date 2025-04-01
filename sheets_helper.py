import gspread
from google.oauth2.service_account import Credentials

SHEET_NAME = "IPTV"
SHEET_TAB = "Klientet"

def get_sheet():
    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    creds = Credentials.from_service_account_file("creds/credentials.json", scopes=scope)
    client = gspread.authorize(creds)
    sheet = client.open(SHEET_NAME).worksheet(SHEET_TAB)
    return sheet

def add_record(record):
    sheet = get_sheet()
    sheet.append_row(record)

def get_records():
    sheet = get_sheet()
    return sheet.get_all_records()

def update_record(row_index, new_data):
    sheet = get_sheet()
    # Build range: A{row+2}:I{row+2}, assuming 9 columns (A to I)
    start_cell = f"A{row_index + 2}"
    end_col_letter = chr(ord("A") + len(new_data) - 1)  # handles A–Z only
    end_cell = f"{end_col_letter}{row_index + 2}"
    cell_range = f"{start_cell}:{end_cell}"
    sheet.update(cell_range, [new_data])  # ✅ fast batch update

def delete_record(row_index):
    sheet = get_sheet()
    sheet.delete_rows(row_index + 2)
