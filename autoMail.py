from dotenv import load_dotenv
from mailjet_rest import Client
import pandas as pd
import os
import datetime 

load_dotenv()

api_key = os.environ['MJ_APIKEY_PUBLIC']
api_secret = os.environ['MJ_APIKEY_PRIVATE']
mailjet = Client(auth=(api_key, api_secret), version='v3.1')


def send_mail(recv_data):
    sender_mail = "updates@saharshapts.co.in"
    curr_month  = datetime.datetime.now().strftime('%B')
    months = recv_data.get("months",[])
    if(recv_data['outstanding_bal']==0):
        months = "NA"
    else:
        months = ", ".join(months)

    
    
    # define class for outstanding_bal in html 
    if recv_data['outstanding_bal'] > 0:
        outstanding_bal_class = "due"
        status = "Pending"
    else:
        outstanding_bal_class = "paid"
        status = "Paid"


    # read html
    with open("due_update_template.html", "r") as file:
        html_content = file.read().strip()
        html_content = html_content.format(
            name=recv_data["name"],
            flat_no=recv_data["flat_no"],
            outstanding_bal=recv_data["outstanding_bal"],
            month= curr_month,
            outstanding_bal_class=outstanding_bal_class,
            status=status,
            months = months
        )

    data = {
        'Messages': [
                        {
                            "From": { "Email": sender_mail , "Name": "Saharsh Association"},
                            "To": [
                                    { "Email": recv_data["email_id"], "Name": recv_data["name"]}
                            ],
                            "Subject": f"Outstanding Balance for {curr_month}",
                            "TextPart": f"Outstanding Balance for {curr_month}",
                            "HTMLPart": html_content
                        }
                ]
        }
    result = mailjet.send.create(data=data)
    response = result.json()
    status = response['Messages'][0]['Status']
    to_email = response['Messages'][0]['To'][0]['Email']  
    if status == 'success':
        # print("Email sent successfully!")
        pass
    else:
        print(f"Failed to send email to {to_email}.")

def process_data(file_path):
    df = pd.read_excel(file_path)

    month_order = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

    df.columns = df.columns.str.strip()
    df['month'] = pd.Categorical(df['month'], categories=month_order, ordered=True)
    df = df.sort_values(by=['flat_no', 'month'])
    flat_array = []  
    last_flat_no = None 
    temp_flat = {} 

    for index, row in df.iterrows():
        if last_flat_no != row['flat_no']:

            if last_flat_no is not None:
                flat_array.append(temp_flat)
            
            # Reset the temp dictionary when flat_no changes
            temp_flat = {}
            temp_flat = {
                "name": row['name'],
                "email_id": row['email_id'],
                "flat_no": row['flat_no'],
                "outstanding_bal" : 0,
                "months": [],  
                "due_dates": [],  
                "due_amounts": []  

            }
        
        # Append
        temp_flat["months"].append(row['month'])
        temp_flat["due_dates"].append(row['due_date'])
        temp_flat["due_amounts"].append(row['due_amt'])
        temp_flat["outstanding_bal"] += row['due_amt'] 
        
        last_flat_no = row['flat_no']

    if temp_flat:
        flat_array.append(temp_flat)

    return flat_array








excel_file = "Book1.xlsx"
flats_data = process_data(excel_file)
for flat in flats_data[:5]:
    send_mail(flat)






