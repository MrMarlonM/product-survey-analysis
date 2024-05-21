import requests
import pandas as pd
from io import BytesIO

def get_user_input():
    """
    Gets the input from the user and checks for possible errors
    happening whilst loading like a wrong url and whilst parsing
    like a wrong format. Afterwards it returns the raw data
    """
    print("You need to put in the url of your survery data file")
    print("It needs to be the url to the raw data")
    print("The file needs to be in the format CSV (Comma-Separated Values)")
    url = input('Put in your URL here:')

    try:
        print("Loading your file...\n")
        response = requests.get(url)
        response.raise_for_status()
        
        raw_data = pd.read_csv(BytesIO(response.content))
        print("The file was loaded successfully!\n")
        return(raw_data)
    except requests.exceptions.RequestException as e:
        print(f"Couldn't download file. Please make sure URL is correct: {e}")
        return None
    except pd.errors.ParserError as e:
        print(f"Couldn't read file. Please ensure the file is in CSV format and try again: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None


def check_data(data):


def main():
    raw_data = get_user_input()
    clean_data = check_data(raw_data)

main()
