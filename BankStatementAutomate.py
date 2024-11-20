import pandas as pd
from openpyxl import Workbook
from datetime import datetime

#for environment variables
from dotenv import load_dotenv
load_dotenv()
import os


def find_name(desc):
    '''Takes description in bank statement and returns name of the payee'''
    # UPI/CR/
    name = ""
    if desc[:7]=="UPI/CR/":
        name = desc.split("/")[3]
    
    # NEFT Cr
    elif desc[:8]=="NEFT Cr-":
        name = desc.split("-")[3]
    
    # MOB-IMPS-CR
    elif desc[:12]=="MOB-IMPS-CR/":
        name = desc.split("/")[1]
    
    # MB
    elif desc[:2]=="MB":
        name = desc.split("/")[2]
    
    # INET-IMPS-CR/
    elif desc[:13]=="INET-IMPS-CR/":
        name = desc.split("/")[1]
    
    # funds transfer
    elif desc[:15]=="Funds Transfer ":
        name = desc.split("-")[-1]
    
    # cash deposit
    elif desc[:13]=="Cash Deposit " :
        name = desc.split("-")[-1]
        
    return name


# Create a new workbook and select the active sheet
wb = Workbook()
ws = wb.active

# Set a title for the sheet
current_date = datetime.now()
month = current_date.strftime('%b-%y').upper()
ws.title = f"Maintenance-{month}"

maintenance_amt = int(os.getenv("MAINTENANCE_AMT"))
bank_statement_location = os.getenv("BANK_STATEMENT_LOCATION")
bank_statement_location = r"{}".format(bank_statement_location)


# Read the Excel file
df = pd.read_excel(bank_statement_location)

# Write headers to the first row
ws.append(["Txn Date", "Value Date", "Name", "Flat No", "Description", "Branch Code", "Credit", "R.NO", "R.DATE"])


names_not_retrieved = 0
names_retrieved = 0
for index, row in df.iterrows():
    amt = row["Credit"]
    
    # Check if the amount is divisible by maintenance_amt
    if amt % maintenance_amt == 0:
        # print(index, row["Description"], amt)
        
 
        #convert to date format
        txn_date = pd.to_datetime(row["Txn Date"], errors='coerce').strftime('%Y-%m-%d') if pd.to_datetime(row["Txn Date"], errors='coerce') else "Invalid Date"
        value_date = pd.to_datetime(row["Value Date"], errors='coerce').strftime('%Y-%m-%d') if pd.to_datetime(row["Value Date"], errors='coerce') else "Invalid Date"

        #find name
        name = find_name(row["Description"])

        if name == "":
            names_not_retrieved += 1
        else:
            names_retrieved += 1

        #find flat num - add logic later
        flat_no = row["FLAT NO"]

        # Append the row to the new sheet
        ws.append([
            txn_date,
            value_date,
            name,
            flat_no,
            row["Description"],
            row["Branch Code"],
            row["Credit"],
            row["R.NO"],
            row["R.DATE"]
        ])

# Save the workbook to a file
wb.save("payments_record.xlsx")
wb.close()

print(f"Names retrieved: {names_retrieved}")
print(f"Names failed to retrieve: {names_not_retrieved}")
print("Check payment_record.xlsx and verify before proceeding")





