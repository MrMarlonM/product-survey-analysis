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
    
    # Try part requests the data from stated url and checks if the HTTP status
    # is in the success range 
    # Uses pandas and to read the content of page and BytesIO to convert bytes
    # sent from the url in readable format for pandas
    try:
        print("Loading your file...\n")
        response = requests.get(url)
        response.raise_for_status()
        
        raw_data = pd.read_csv(BytesIO(response.content))
        print("The file was loaded successfully!\n")
        return(raw_data)
    
    # Displays error when something goes wrong with the HTTP request like a wrong
    # URL or a timeout
    except requests.exceptions.RequestException as e:
        print(f"Couldn't download file. Please make sure URL is correct: {e}")
        return None
    
    # Displays error when file isn't correctly structured or data type is wrong
    except pd.errors.ParserError as e:
        print(f"Couldn't read file. Please ensure the file is in CSV format and try again: {e}")
        return None
    
    # Displays all errors that could happen and aren't catched before
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None


def check_data(data):
    """
    Checks if the provided data is eligible for analysis. 
    Checks for product column and that there is at least one question column.
    Checks that the answers are in the allowed range.
    Removes rows with invalid data and rows with missing data
    """
    print("Checking and cleaning the data...")

    try:
        # Checks with two if statements that "Products" column exists and questions exist
        if "Product" not in data.columns:
            raise ValueError("The product column is missing, please add one")
        if len(data.columns) < 2:
            raise ValueError("There are no questions in the data, please add at least one")  
        
        # The allowed answers for the survey can be changed here
        allowed_answers = ["Very unhappy", "Unhappy", "Happy", "Very happy"]
        
        # Checks that the provided answers are part of the allowed options
        # for every column exept the "Product" column
        for col in data.columns.drop("Product"):
            data = data[data[col].isin(allowed_answers)]

        # Remove rows where values are missing
        data.dropna(inplace=True)

        return data
    
    # Returns one of the defined ValueError catched by the two if functions
    except ValueError as e:
        print(f"Error in data: {e}")
        return None
    
    # Returns every unexpected error
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None


def main():
    """
    Runs the program and summons all the needed functions in the correct order
    """
    raw_data = get_user_input()
    print(raw_data)
    clean_data = check_data(raw_data)
    print(clean_data)
main()
