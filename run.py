import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('love_sandwiches')

def get_sales_data():
    """
    Get sales figures from spreadsheet
    """
    while True:
        print("Please enter sale data from the last market.")
        print("Data should be six numbers, separated by commas.")
        print("e.g. 10,20,30,40,50,60\n")

        data_str = input("Data: ")
        sales_data = data_str.split(",")
        validate_data(sales_data)
        
        if validate_data(sales_data):
            print("Data accepted, thank you.")
            break
    return sales_data

def validate_data(values):
    """
    Inside the try, converts all string values into integers.
    Raises ValueError if strings cannot be converted into int,
    or if there aren't exactly 6 values.
    """
    try:
        [int(value) for value in values]
        if len(values) != 6:
            raise ValueError(
                f"Exactly 6 values required, you provided {len(values)}"
            )
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")
        return False
    return True

def update_sales_worksheet(data):
    """
    Update the sales worksheet, add new row with the list data provided.
    """
    print("Updating sales worksheet... \n")
    sales_worksheet = SHEET.worksheet("sales")
    sales_worksheet.append_row(data)  
    print("Sales worksheet updated successfully.\n")


data = get_sales_data()
sales_data = [int(num) for num in data]
update_sales_worksheet(sales_data)