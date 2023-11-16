import os
import json
import requests
from requests.exceptions import Timeout
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

# Secect the value (0 = False, 1 = True)
MAIL_CUSTOM = os.getenv('MAIL_CUSTOM')
MAIL_SEND_EVERY_TIME = os.getenv('MAIL_SEND_EVERY_TIME')
MAIL_TO_ADDRESS_HIDE = os.getenv('MAIL_TO_ADDRESS_HIDE')

if MAIL_CUSTOM == "1":
   MAIL_SUBJECT = os.getenv('MAIL_SUBJECT')
   MAIL_BODY_HTML = os.getenv('MAIL_BODY_HTML')
   MAIL_BODY_TEXT = os.getenv('MAIL_BODY_TEXT')
   MAIL_SUBJECT_NOT_CHANGED = os.getenv('MAIL_SUBJECT_NOT_CHANGED')
   MAIL_BODY_HTML_NOT_CHANGED = os.getenv('MAIL_BODY_HTML_NOT_CHANGED')
   MAIL_BODY_TEXT_NOT_CHANGED = os.getenv('MAIL_BODY_TEXT_NOT_CHANGED')
else:
   MAIL_SUBJECT = "CIS IPS Changed."
   MAIL_BODY_HTML = "<strong>CIS IPS has been changed.</strong><br>Please check your access-lists."
   MAIL_BODY_TEXT = "CIS IPS has been changed.\nPlease check your access-lists.\nThis is a text mail."
   MAIL_SUBJECT_NOT_CHANGED = "CIS IPS not Changed."
   MAIL_BODY_HTML_NOT_CHANGED = "This is a user-edited mail."
   MAIL_BODY_TEXT_NOT_CHANGED = "This is a user-edited mail.\nThis is a text mail."

if MAIL_TO_ADDRESS_HIDE == "1":
   address_hide = True
else:
   address_hide = False

MAIL_ADDRESS_TO = [m.strip() for m in os.getenv('MAIL_ADDRESS_TO').split(',')]
print(MAIL_ADDRESS_TO)

print("MAIL_ADDRESS_FROM : ",os.getenv('MAIL_ADDRESS_FROM'))
print("MAIL_ADDRESS_TO : ",os.getenv('MAIL_ADDRESS_TO'))

print("MAIL_CUSTOM : ",MAIL_CUSTOM)
print("MAIL_SEND_EVERY_TIME : ",MAIL_SEND_EVERY_TIME)
print("MAIL_TO_ADDRESS_HIDE : ",MAIL_TO_ADDRESS_HIDE,address_hide)
   
message = Mail(
    from_email=os.getenv('MAIL_ADDRESS_FROM'),
    to_emails=MAIL_ADDRESS_TO,
    subject=MAIL_SUBJECT,
    html_content=MAIL_BODY_HTML,
    plain_text_content=MAIL_BODY_TEXT,
    is_multiple=address_hide)
    
message_not_changed = Mail(
    from_email=os.getenv('MAIL_ADDRESS_FROM'),
    to_emails=MAIL_ADDRESS_TO,
    subject=MAIL_SUBJECT_NOT_CHANGED,
    html_content=MAIL_BODY_HTML_NOT_CHANGED,
    plain_text_content=MAIL_BODY_TEXT_NOT_CHANGED,
    is_multiple=address_hide)

try:
  url = "https://api.cis.cloud.ibm.com/v1/ips"
  r = requests.get(url, timeout=3.0)
  
  if r.status_code != 200:
     print("status_code from cis-ips was not 200.")
  
  elif r.json()["result"]["etag"] == os.getenv('ETAG'):
     print("There is no difference.")
     if MAIL_SEND_EVERY_TIME == "1":
         sg = SendGridAPIClient(os.getenv('SENDGRID_API_KEY'))
         response = sg.send(message_not_changed)
         print(response.status_code)
         print(response.body)
         print(response.headers)
  
  else:
     print("There is difference. CIS IPS has been changed.")
     sg = SendGridAPIClient(os.getenv('SENDGRID_API_KEY'))
     response = sg.send(message)
     print(response.status_code)
     print(response.body)
     print(response.headers)
  
except Timeout:
  print("timeout.")
  pass