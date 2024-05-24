import requests
import pandas as pd
from io import BytesIO
import validators
from simple_term_menu import TerminalMenu

def get_user_input():
    """
    Gets the input from the user and checks for possible errors
    happening whilst loading, like a wrong url and whilst parsing
    like a wrong format. Afterwards it returns the raw data
    """
    # Loops and asks for url until valid url is given as input
    while True:
        print(f"""
You need to put in the direct URL to your survey data, stored publicly.
The link must provide the raw data, not the document to download.
You can use for example github or dropbox and click on "raw data" to open the 
right URL. 
The file needs to be formatted as CSV (Comma-Separated Values).
After providing the file, the analysis will run and put out the calculated values.
        """)
        url = input('Put in your URL here:')
        
        if validators.url(url):
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
                return raw_data
            
            # Displays error when something goes wrong with the HTTP request like a wrong
            # URL or a timeout
            except requests.exceptions.RequestException as e:
                print(f"Couldn't download file. Please make sure URL is correct: {e}")
                return None
            
            # Displays error when file isn't correctly structured or data type is wrong
            except pd.errors.ParserError as e:
                print(f"Couldn't read file. Please ensure the file is a CSV file and try again: {e}")
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
        allowed_answers = ["Very unhappy", "Unhappy", "Neutral", "Happy", "Very happy"]
        
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
    The function transforms text data into numerical values
    to calculate values
    """
    # Extra answer options need to be added here together with numerical value
    new_data = data.copy()
    for col in data.columns.drop("Product"):
        new_data[col] = new_data[col].replace(
            ["Very unhappy", "Unhappy", "Neutral", "Happy", "Very happy"], [1, 2, 3, 4, 5]
        )
    return new_data


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


def print_legend():
    print(f"""
Legend for results of analysis:\n
    1 = Very unhappy
    2 = Unhappy
    3 = Neutral
    4 = Happy
    5 = Very happy\n
    """)


def calculate_mean_questions(data):
    """
    Function to calculate the mean value for the answers given for each question
    and prints the mean values to the console next to the questions
    """
    print("Calculating mean values for individual questions...\n")

    mean_questions = data.drop(columns=["Product"]).mean()
    
    print(f"""
Here are the mean values for each question:\n
{mean_questions}\n
    """)


def find_mode_questions(data):
    """
    Function to find the mode for each question asked, and print the findings
    to the console in a readable and clean manner
    """
    print("Finding mode for each question...\n")
    mode_questions = data.drop(columns=["Product"]).mode()
    # Prints the mode for each question more readable to the console than the 
    # Dataframe that gets returned to mode_questions
    print("Here is the mode for each question:\n")
    for question, mode in mode_questions.iloc[0].items():
        print(f"{question}: {mode}")
    print("\n")


def calculate_mean_products(data, list_products):
    """
    The function calculates the mean over all questions for each each seperate
    product and gives the values out to the terminal
    """
    print("Calculating mean values for each product...\n")

    mean_products = {}
    for product in list_products:
        # Creates new dataframe where only the rows of the wanted product are left
        product_row = data[data["Product"] == product].drop(columns=["Product"])
        # Calculates the mean for each row and then the mean of the means of each row
        mean_product = product_row.mean(axis=1).mean()
        mean_products[product] = mean_product
    
    print(f"""
Here are the mean values for each product:\n
{pd.Series(mean_products)}\n
    """)


def find_mode_products(data, list_products):
    """
    This function finds the mode for each product and
    gives them out to the terminal
    """
    print(f"""
Finding the mode for each product...\n
Here is the mode for each product:\n
    """)

    for product in list_products:
        product_row = data[data["Product"] == product].drop(columns=["Product"])
        all_rows = product_row.stack()
        mode_product = all_rows.mode()[0]
        print(f"{product}: {mode_product}")


def start_analysis(num_data, clean_data, list_products):
    """
    This function analyzes the data and calculates the mean and mode for each 
    question and product. It also provides a menu where the user can choose to 
    watch each analysis individually or to insert a new file for analysis
    """
    #Deefine parameters for sub menu and back menu/button
    sub_options = ["[q] Analysis Questions", "[p] Analysis Products", "[n] Insert new File"]
    back_sub = ["[b] Back to Sub Menu"]
    sub_menu = TerminalMenu(sub_options)
    back_sub_menu = TerminalMenu(back_sub)
    # Show submenu for individual analysis
    sub_menu_index = sub_menu.show()
    sub_menu_choice = sub_options[sub_menu_index]
    # Start analysis for questions
    if sub_menu_choice == "[q] Analysis Questions":
        print_legend()
        calculate_mean_questions(num_data)
        find_mode_questions(clean_data)
        back_sub_index = back_sub_menu.show()
        back_sub_choice = back_sub[back_sub_index]
        # Offer option to go back to sub menu
        if back_sub_choice == "[b] Back to Sub Menu":
            start_analysis(num_data, clean_data, list_products)
    # Start analysis for products
    elif sub_menu_choice == "[p] Analysis Products":
        print_legend()
        calculate_mean_products(num_data, list_products)
        find_mode_products(clean_data, list_products)
        back_sub_index = back_sub_menu.show()
        back_sub_choice = back_sub[back_sub_index]
        # Offer option to go back to sub menu
        if back_sub_choice == "[b] Back to Sub Menu":
            start_analysis(num_data, clean_data, list_products)
    # Goes back to main menu to insert new file
    elif sub_menu_choice == "[n] Insert new File":
        main()


def main():
    """
    Runs the program and summons all the needed functions
    in the correct order
    """
    # Welcome statement and explanation what the user should do
    print(f"""
Hello and welcome to the product-survey-analysis!
If you already now how it works click on "Start"
or press the "s" button on your keyboard.
Should it be your first time, click on "Show Explanation"
or press the "e" button on your keyboard.
    """)
    #Definition of options for different terminal menus
    main_options = ["[s] Start", "[e] Show Explanation"]
    back_main = ["[b] Back to Main Menu"]
    
    # Declares the different terminal menus
    main_menu = TerminalMenu(main_options)
    back_main_menu = TerminalMenu(back_main)

    # Starts the Main Menu 
    main_menu_index = main_menu.show()
    main_menu_choice = main_options[main_menu_index]
    # Start the analysis
    if main_menu_choice == "[s] Start":
        # Get data from user and prepare data for analysis
        raw_data = get_user_input()
        clean_data = check_data(raw_data)
        return_questions(clean_data) 
        list_products = count_products(clean_data)
        num_data = transform_data(clean_data)
        #Analyze the given data
        start_analysis(num_data, clean_data, list_products)
    # Shows the explanation how to use the program properly
    elif main_menu_choice == "[e] Show Explanation":
        print(f"""
1. You need to put in the direct URL to your survey data, which should be
    stored publicly aviable.

2. The link must provide the raw data, not the document to download.
    You can use for example github or dropbox and click on "raw data" to open the 
    right URL. 

3. The file needs to be formatted as CSV (Comma-Separated Values).
    After providing the file, the analysis will run and put out the calculated values.
        """)
        print_legend()
        #Offer a menu/button to go back to main menu
        back_main_menu_index = back_main_menu.show()
        back_main_menu_choice = back_main[back_main_menu_index]
        if back_main_menu_choice == "[b] Back to Main Menu":
            main()


#Start the program
if __name__=="__main__":
    main()
