#from twilio.rest import Client

# Replace these with your Twilio credentials
#account_sid = 'your_account_sid'  # Replace with your actual SID
#auth_token = 'your_auth_token'  # Replace with your actual Auth Token

#client = Client(account_sid, auth_token)

#def send_sms(to_number, message_body):
#    message = client.messages.create(
#        body=message_body,
#        from_='+your_twilio_phone_number',  # Replace with your Twilio phone number
#        to=to_number
#    )
#    return message.sid

from twilio.rest import Client

account_sid = 'AC2494c277750c1a1601be8116f3eaac6f'
auth_token = '[AuthToken]'
client = Client(account_sid, auth_token)
def send_sms(to_number, message_body):
    message = client.messages.create(
      body=message_body,  
      from_='+16282579501',
      to='+917796779022'
    )
    return message.sid


#Dnyanendra_@2122
#JH8WYR7LARQHC2KEGLE5L18X
