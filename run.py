import requests
import pandas as pd
from io import BytesIO

def get_user_input():
    print("You need to put in the url of a raw file in the format CSV")
    url = input('Put in your URL here:\n')

    response = requests.get(url)

    raw_data = pd.read_csv(BytesIO(response.content))
    return(raw_data)
