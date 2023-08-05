# strip-spreadsheet
This tool is for working with spreadsheets.
It cleans the spreadsheet off of any rows that have blank data in them and removes extra-spaces.

## Installation
This is OS independent, meaning it won't need a specific Os to run on.

You can install the strip-spreadsheet package simply by running:
```shell
pip install strip-spreadsheet
```

## Sample Code
```python
from strip_spreadsheet import clean_sheet


# open the dirty sheet as a readable file
with open('x.csv', 'r') as dirty_sheet:
    # put all the rows in the sheet in a list
    unclean_sheet = dirty_sheet.readlines()
    
    # open the file wanna save the cleaned sheet to
    with open('x_cleaned.csv', 'w') as cleaned_up_sheet:
        # clean the unclean sheet and write the output to the new file we created
        cleaned_up_sheet.writelines(clean_sheet(unclean_sheet))
```