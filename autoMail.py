from dotenv import load_dotenv
from mailjet_rest import Client
import os
load_dotenv()

api_key = os.environ['MJ_APIKEY_PUBLIC']
api_secret = os.environ['MJ_APIKEY_PRIVATE']
mailjet = Client(auth=(api_key, api_secret), version='v3.1')



def Send_mail(recv_data):
    sender_mail = "updates@saharshapts.co.in"
    recv_data["mail_id"] = "ntshrihari@gmail.com"
    
    ''' template contains : 
        {name}} , {{flat_no}} , {{outstanding_bal}}: Outstanding balance
        {{month}} The month for which the maintenance payment is due , {{year}} '''
    
    # define class for outstanding_bal in html 
    if recv_data['outstanding_bal'] > 0:
        outstanding_bal_class = "due"
        status = "Pending Due"
    else:
        outstanding_bal_class = "paid"
        status = "Paid"


    # read html
    with open("test_template.html", "r") as file:
        html_content = file.read().strip()
        html_content = html_content.format(
            name=recv_data["name"],
            flat_no=recv_data["flat_no"],
            outstanding_bal=recv_data["outstanding_bal"],
            month=recv_data["month"],
            outstanding_bal_class=outstanding_bal_class,
            status=status
        )

    data = {
        'Messages': [
                        {
                            "From": {
                                    "Email": sender_mail ,
                                    "Name": "Saharsh Association"
                            },
                            "To": [
                                    {
                                            "Email": recv_data["mail_id"],
                                            "Name": recv_data["name"]
                                    }
                            ],
                            "Subject": f"Outstanding Balance for {recv_data['month']}",
                            "TextPart": f"Outstanding Balance for {recv_data['month']}",
                            "HTMLPart": html_content
                        }
                ]
        }
    result = mailjet.send.create(data=data)
    # print(result.json())
    res_data = result.json()        




test_data = [ {"name": "John Doe", "flat_no": "A-305", "outstanding_bal": 500, "month": "December"}, 
             {"name": "Jane Smith", "flat_no": "B-102", "outstanding_bal": 0, "month": "December"}, 
             {"name": "Raj Kumar", "flat_no": "C-204", "outstanding_bal": -1500, "month": "November"}, 
             {"name": "Priya Sharma", "flat_no": "D-401", "outstanding_bal": 250, "month": "October"}, 
             {"name": "Anil Gupta", "flat_no": "E-507", "outstanding_bal": 800, "month": "December"} ]

for record in test_data:
    print(record)
    Send_mail(record)





