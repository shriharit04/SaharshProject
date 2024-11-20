from twilio.rest import Client
from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

#init twilio api
account_sid = 'AC4386a73f839359e8df9cbe01853b513b'
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
client = Client(account_sid, auth_token)



#sending message
variable_1 = "trial" 
variable_2 = "data"  
message = client.messages.create(
    from_='whatsapp:+14155238886',
    content_sid='HXb5b62575e6e4ff6129ad7c8efe1f983e',
    content_variables=f'{{"1":"{variable_1}","2":"{variable_2}"}}',
    to='whatsapp:+919791441419'
)


print(message.sid)