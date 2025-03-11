import os
import gspread
from google.oauth2.service_account import Credentials

SCOPE = ["https://www.googleapis.com/auth/spreadsheets"]
SHEET_ID = "13mCs-Vwv4EbT2ANuykpIL2_hr1ZghabkWSEmEkwc0cw"

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
CREDENTIAL_FILE = os.path.join(CURRENT_DIR, "credentials.json")

CREDENTIALS = Credentials.from_service_account_file(CREDENTIAL_FILE, scopes = SCOPE)
CLIENT = gspread.authorize(CREDENTIALS)
WORKBOOK = CLIENT.open_by_key(SHEET_ID)

worksheet_list = map(lambda x: x.title, WORKBOOK.worksheets())
worksheet_name = "applicant_details"
 
# check worksheet already exists or not
def check_worksheet_existance() -> object :
    if worksheet_name in worksheet_list :
        # access the sheet need to update
        sheet = WORKBOOK.worksheet(worksheet_name)
    else :
        # create sheet for updates
        sheet = WORKBOOK.add_worksheet(worksheet_name, rows=100, cols=10)

    return sheet


# update google sheet with the applicant details
def update_google_spread_sheet(name:str, mail:str, contact:str, education:str, qualification:str, experience:str) -> bool:
    sheet = check_worksheet_existance()

    all_values = sheet.get_all_values()
    row_count = len(all_values)
    next_row = int(row_count) + 1

    # Write data in the google spreadsheet
    try :
        sheet.update_cell( next_row,1, name )
        sheet.update_cell( next_row,2, mail )
        sheet.update_cell( next_row,3, contact)
        sheet.update_cell( next_row,4, education )
        sheet.update_cell( next_row,5, qualification )
        sheet.update_cell( next_row,6, experience )

        return True
    except: 
        print("Something went wrong")
        return False