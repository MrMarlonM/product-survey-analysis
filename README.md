# Product Survey Analysis
This program will help you analyze your product survey for you!  
Just provide your CSV file with the raw data and wait for the program to
calculate the information you need. 

## User Stories
### First Time Visitor
- I want to understand the purpose of the program
- I want to be able to directly start analyzing some data
- I want to get a clear and concise instruction

### Frequent Visitor 
- I want to analyze more surveys easily
- I want to download the result
- I want to get a more in-depth analysis

## Data Requirements
- The survey data needs to be in CSV (Comma-Separated-Values) format.
- The data needs to be provided as a URL.
- The URL needs to link directly to the raw data on a publicly available site like Github or Dropbox for example.
- The "Product" column and answer options are case-sensitive!
- The first row is for the heading with:
    - One column that is named "Product". (required)
    - One or more questions that are written directly in the heading. (min. 1)
- The allowed answer options for this version are:
    - Very unhappy
    - Unhappy
    - Happy
    - Very happy

## Bugs
### Solved Bugs
- Bug 1: Whilst testing the `get_user_input() function` and the `check_data() function` combined, a set of data that had no answer options in it got returned. After checking that the data returned from the `get_user_input() function` was correct, the problem could be narrowed down to the `check_data() function`. After checking that the code is correct and contains no typos, the error was found in the case sensitivity of the `allowed_answer list` and the data input it got compared against.  
Solution: the problem was solved for this version by changing the content of the `allowed_answer_list` so that it matches the data. Also, the exact kind of data expected by the program gets stated in the readme under the point `Data Requirements`.