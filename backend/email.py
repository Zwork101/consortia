import base64
from email.message import EmailMessage
import os

from flask import Blueprint

from .auth import admin_required
from .db import Token, commit

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/gmail.send']


def get_token(org: int) -> tuple[Credentials, str] | None:
   token = Token.query.filter(Token.org_id == org).limit(1).first()

   if token is None:
      return None

   cred = Credentials.from_authorized_user_info({
      "token": token.token,
      "refresh_token": token.refresh_token,
      "token_uri": token.token_uri,
      "client_id": token.client_id,
      "client_secret": token.client_secret,
      "expiry": token.expirey.isoformat()

   }, scopes=SCOPES)

   if not cred.valid:
      return None

   if cred.expired:
      cred.refresh(Request())
      token.token = cred.token
      commit(token)

   return cred, token.email


def send_email(content: str, subject: str, source_email: str, bcc_emails: list[str], cred: Credentials):
   service = build("gmail", "v1", credentials=cred)

   message = EmailMessage()
   message.set_content(content, subtype="html")
   message["From"] = source_email
   message["Subject"] = subject
   message["bcc"] = ", ".join(bcc_emails)

   encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

   create_message = {"raw": encoded_message}
   return service.users().messages().send(userId="me", body=create_message).execute()
