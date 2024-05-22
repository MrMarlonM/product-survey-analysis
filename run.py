import requests
import pandas as pd
from io import BytesIO

def get_user_input():
    """
    Gets the input from the user and checks for possible errors
    happening whilst loading, like a wrong url and whilst parsing
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
    print("Checking and cleaning the data...\n")

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

        print("Great, your data is now clean and ready for analysis.\n")
        return data
    
    # Returns one of the defined ValueError catched by the two if functions
    except ValueError as e:
        print(f"Error in data: {e}")
        return None
    
    # Returns every unexpected error
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None


# This line of code opts-in to a future change how pandas handles downcasting
# with this line of code the "FutureWarning:.." in the terminal doesn't get shown
pd.set_option('future.no_silent_downcasting', True)
def transform_data(data):
    """
    The function transforms text data into numerical values to calculate values
    """
    for col in data.columns.drop("Product"):
        data[col] = data[col].replace(
            ["Very unhappy", "Unhappy", "Happy", "Very happy"], [1, 2, 3, 4]
        )
    return data


def return_questions(data):
    """
    This function will count the number of questions in the provided data and
    return the number of questions asked together with the individual questions 
    to the terminal
    """
    print("Here is an overview of the data provided:\n")

    number_questions = len(data.columns) - 1
    print(f"Your survey asks {number_questions} different questions:")
    
    i = 1
    for col in data.columns.drop("Product"):
        print(f"Question{i}: {col}")
        i += 1
    print("\n")


def count_products(data):
    """
    Takes the products column of the provided data and returns a list of every
    individual product listed in the data
    """
    list_products = data['Product'].unique().tolist()
    counter = 1
    print("The following products are part of your survey:")
    for product in list_products:
        print(f"Product {counter}: {product}")
        counter +=1
    print("\n")    
    return list_products


def calculate_mean_questions(data):
    """
    Function to calculate the mean value for the answers given for each question
    and gives out a pandas series with the calculated values
    """
    print("Calculating mean values for individual questions...\n")

    mean_questions = data.drop(columns=["Product"]).mean()
    return mean_questions


def main():
    """
    Runs the program and summons all the needed functions in the correct order
    """
    raw_data = get_user_input()
    clean_data = check_data(raw_data)
    return_questions(clean_data) 
    list_products = count_products(clean_data)
    num_data = transform_data(clean_data)
    mean_questions = calculate_mean_questions(num_data)
    print(mean_questions)
    

main()
