# NOTE : 
## For cash Transactions, save Description manually as 
``` Cash - <payee name> ```

## The Code doesnt guarantee retrieval of 100% of the payee names. It only guarantees the accuracy of the retreived names. Hence a final review of the excel sheet is required.

## Project Overview
- This script processes the bank statement in Excel format and extracts maintenance payment details and creates a new Excel file with the extracted data. 
- The extracted data includes transaction date, value date, name of the payee, flat number, description, branch code, credit amount, and other details. 
- It also find the name of the payee from the desc.
- It does not modify the original bank statement



# Setup
Python 3.x must be installed

## Pre processing Bank Statement
Make sure that the first line of the excel sheet is the column headings. Delete all data above it.

### Windows
```
python -m venv venv
venv\Scripts\Activate
```

### MacOS / Ubuntu
```
python -m venv venv
source venv/bin/activate
```

## Create .env file with the following values

```
MAINTENANCE_AMT: <current maintenance amount>
BANK_STATEMENT_LOCATION: <path to bank statement>.
```

## Example .env file:

```
MAINTENANCE_AMT = 3500
BANK_STATEMENT_LOCATION = C:\Users\Shrihari\Downloads\can bank statements.xlsx
```



# Functionality
- Read Bank Statement: The script loads the bank statement Excel file specified by the BANK_STATEMENT_LOCATION environment variable.
- Find Payee Name: Based on the description of the transaction, the script determines the name of the payee using predefined patterns.
- Filtering Payments: The script filters transactions where the credit amount is divisible by the MAINTENANCE_AMT specified in the .env file.
- Generate Report: A new Excel workbook is created, and the relevant data is written to it. 

**Output Format**: The generated Excel file contains the following columns:


The script will create a file named payments_record.xlsx  containing the filtered and structured payment data in the same folder as the progrma.


### Notes
- The script assumes that the bank statement contains the columns Txn Date, Value Date, Description, FLAT NO, Branch Code, Credit, R.NO, and R.DATE. Ensure that the input file follows this structure.
- The logic to find the flat number from the bank statement can be expanded or customized based on further requirements.

