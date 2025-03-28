import os
from flask import Blueprint, session, current_app, abort, url_for, redirect, request
from flask_login import current_user

from backend.email import SCOPES
from backend.auth import admin_required
from backend.db import Token, commit

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow

CLIENT_SECRETS_FILE = "client_secret.json"

oauth = Blueprint("oauth", __name__, static_folder="/static", template_folder="/templates")


def url_for_redirect(flow: Flow) -> str:
   authorization_url, state = flow.authorization_url(
      access_type='offline',
      include_granted_scopes='true',
      login_hint=current_user.email,
      prompt='consent'
   )
   session['state'] = state
   return authorization_url


@oauth.route("/authorize/<int:org>")
@admin_required
def authorize_email(org: int):
	flow = Flow.from_client_secrets_file(CLIENT_SECRETS_FILE, scopes=SCOPES)
	flow.redirect_uri = url_for("oauth.callback", _external=True)
	print(flow.redirect_uri)

	session['email_auth'] = [org, current_user.email]

	return redirect(
		url_for_redirect(flow)
	)

@oauth.route("/email/oauth2callback")
@admin_required
def callback():
	state = session['state']

	flow = Flow.from_client_secrets_file(CLIENT_SECRETS_FILE, scopes=SCOPES, state=state)
	flow.redirect_uri = url_for('oauth.callback', _external=True)
	print(flow.redirect_uri)

	authorization_response = request.url
	flow.fetch_token(authorization_response=authorization_response)

	t = Token(
		org_id = session['email_auth'][0],

		token = flow.credentials.token,
		refresh_token = flow.credentials.refresh_token,
		token_uri = flow.credentials.token_uri,
		client_id = flow.credentials.client_id,
		client_secret = flow.credentials.client_secret,
		expirey = flow.credentials.expiry,

		email = session['email_auth'][1]
	)
	commit(t)
	return "Oauth2 dance complete"