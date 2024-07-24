import base64
from django.contrib.auth import get_user_model
import msal
import requests
from decouple import config
from rest_framework.utils import json

User = get_user_model()
# Enter the details of your AAD app registration
client_id = config("CLIENT_ID")
client_secret = config("CLIENT_SECRET")
tenant_id = config("TENANT_ID")

authority = f'https://login.microsoftonline.com/{tenant_id}'
scope = ['https://graph.microsoft.com/.default']
user_id = config("SEND_EMAIL_USER_ID")

app = msal.ConfidentialClientApplication(
    client_id=client_id,
    client_credential=client_secret,
    authority=authority)


def get_graph_api_token():
    scopes = ["https://graph.microsoft.com/.default"]
    result = app.acquire_token_silent(scopes, account=None)

    if not result:
        result = app.acquire_token_for_client(scopes=scopes)
    token = result.get('access_token', "")
    return token


def send_email_attachment(to, message_body="", message_subject="", file_data=None, cc=None,
                          reply_to=None):
    if reply_to is None:
        reply_to = []
    if cc is None:
        cc = []
    cc = [user_email for user_email in cc if user_email]
    if file_data is None:
        file_data = []
    headers = {'Authorization': 'Bearer ' + get_graph_api_token(),
               'Content-Type': 'application/json',
               }
    attachment = []
    url = f"https://graph.microsoft.com/v1.0/users/{user_id}/sendMail"
    email_to = [{"emailAddress": {"address": user}} for user in to if user]
    cc_email = [{"emailAddress": {"address": user}} for user in cc if user]
    reply_to = [{"emailAddress": {"address": user}} for user in reply_to if user]

    for data in file_data:
        attachment.append({
            "@odata.type": "#microsoft.graph.fileAttachment",
            "name": data.get("file_name", ""),
            "contentType": data.get("content_type", ""),
            "contentBytes": base64.b64encode(data.get("file_bytes", "")).decode('utf-8')
        })
    body = {
        "message": {
            "subject": message_subject,
            "body": {
                "contentType": "HTML",
                "content": message_body
            },
            "toRecipients": email_to,
            "ccRecipients": cc_email,
            "attachments": attachment,
            "replyTo": reply_to
        }
    }
    response = requests.post(url, json=body, headers=headers)
    status_code = response.status_code
    return status_code, response.text


def send_email_graph_api(subject, body, to):
    # Graph API endpoint to send email
    send_mail_url = f'https://graph.microsoft.com/v1.0/users/{user_id}/sendMail'

    # Headers with authorization and content type
    headers = {
        "Authorization": f"Bearer {get_graph_api_token()}",
        "Content-Type": "application/json"
    }
    email_to = [{"emailAddress": {"address": user}} for user in to.split(",") if user]
    # Email payload
    email_data = {
        'message': {
            'subject': subject,
            'body': {
                'contentType': 'html',
                'content': body
            },
            'toRecipients': email_to,
            'ccRecipients': [],
        }
    }

    # Send the email
    response = requests.post(send_mail_url, headers=headers, data=json.dumps(email_data))
    return response.status_code
