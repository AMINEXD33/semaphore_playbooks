import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import base64
from email.mime.text import MIMEText

SCOPES = ["https://www.googleapis.com/auth/gmail.send"]
TOKEN_PATH = "/home/dxc-network/Bureau/gmail/gmail.json"

def get_credentials():
    creds = None
    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
            with open(TOKEN_PATH, "w") as f:
                f.write(creds.to_json())
        else:
            raise Exception(
                "token.json has no usable refresh_token. "
                "Re-run generate_token.py locally and re-upload."
            )
    return creds

def send_mail(to, subject, body):
    creds = get_credentials()
    service = build("gmail", "v1", credentials=creds)

    message = MIMEText(body)
    message["to"] = to
    message["subject"] = subject
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()

    try:
        service.users().messages().send(userId="me", body={"raw": raw}).execute()
        print("Sent.")
    except HttpError as error:
        print(f"Send failed: {error}")

if __name__ == "__main__":
    send_mail("hooligans.hooligans22@gmail.com", "Test", "Hello from automation")
