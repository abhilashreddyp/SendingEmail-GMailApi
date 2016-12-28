from __future__ import print_function
import httplib2
import os
from apiclient import discovery
from apiclient import errors
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
import base64
from email.mime.text import MIMEText
try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None


SCOPES='https://www.googleapis.com/auth/gmail.compose'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Gmail API Python Quickstart'
MY_ID="ENTER_YOUR_EMAIL_ID_HERE"

#validate your credentials
def get_credentials():
    
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'gmail-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

#Function to dispatch your E-Mail  
def send_message(service, message,senderid):
  try:
    message = (service.users().messages().send(userId=MY_ID, body=message).execute())
    print('\nSending Email to '+senderid+' ....')
    print('Your Mail has been sent successfuly !')
    #print('Message Id is : %s' % message['id'])
    return message
  except errors.HttpError, error:
    print('\nSending Email to '+senderid+' ....')  
    print('\nAn error occurred: %s' % error)

#Function to create your E-Mail
def create_message(service):
    #Creating Recipient List from External File     
     recipients=[]
     f1=open("Email\\emailid.txt","r")
     recipients=f1.readlines()
     for i in range (0,len(recipients)):
         recipients[i]=recipients[i].strip('\n')
         
     #Creating MEssage Body
     f2=open("Email\\email_body.txt","r")
     body=f2.read()
     
     #Preview for COnfirmation
     print('Total Recipients : '+str(len(recipients))+' (Check The Text File for complete list)\n')
     print('Message Preview :\n')
     print("---------------------------")     
     print(body)
     print("---------------------------")
     body=body.replace('\n','<br>')
     
     sender=MY_ID
     subject=raw_input("\nEnter The Subject : \n")
     message_text=body
     
     choice=raw_input('Are you sure you want to send the mail ? Enter "yes"')
     if choice=='yes':
         for i in recipients:     
            message = MIMEText(message_text,'html')
            message['to'] = i
            message['from'] = sender
            message['subject'] = subject
            ready_msg={'raw': base64.urlsafe_b64encode(message.as_string())}
            send_message(service,ready_msg,i)
     
#Main Function 
def main():
    print("------------------------------")
    print("Welcome To Gmail API Program")
    print("------------------------------")
    
    #validate your credentials
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)

    #function to create your function    
    create_message(service)
    print("\n\nHave A Nice Day !!")

if __name__ == '__main__':
    main()
