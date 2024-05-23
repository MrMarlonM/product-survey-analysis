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
    - Neutral
    - Happy
    - Very happy

## Bugs
### Solved Bugs
- *Bug 1:*  
Whilst testing the `get_user_input() function` and the `check_data() function` combined, a set of data that had no answer options in it was returned. After checking that the data returned from the `get_user_input() function` was correct, the problem could be narrowed down to the `check_data() function`. After checking that the code is correct and contains no typos, the error was found in the case sensitivity of the `allowed_answer list` and the data input it got compared against.  
*Solution:*   
The problem was solved for this version by changing the content of the `allowed_answer_list` so that it matches the data. Also, the exact kind of data expected by the program gets stated in the readme under the point `Data Requirements`.

- *Bug 2:*  
The initial version of `return_questions()` was called `count_questions()` and should have counted the number of questions and printed the individual questions to the console. The first part worked, but the second didn't. It only printed a complete list of all column headings to the console, instead of each question separately.
*Solution:*  
To solve the problem, the function was remodeled and simplified. Instead of a `for loop` that counts the number of questions, the length of `data_columns` gets subtracted by one. Also, the fact was used, that the `pandas library` allows it to print out the column heading directly through a `for loop` like this: `for col in data.columns: print col`. 

- *Bug 3:*  
The function `find_mode_questions(clean_data)` returned numerical values instead of a string. The problem could be tracked down to the `transform_data()` function. Here the `clean_data` variable was changed to a numerical value. But because no new variable was assigned the original variable was overwritten.  
*Solution:*
To solve the problem, the data provided to the function was copied to a new variable named `new_variable`. Then it was transformed and returned. With that, both sets of data, one with strings and one with integers, stay in existence.