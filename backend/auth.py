from .db import Profile, db, commit

from flask import Request
import flask_login

shib = flask_login.LoginManager()


@shib.request_loader
def request_loader(request: Request):
	user = Profile.query.where(Profile.rit_id == request.environ["uid"]).first()

	if user is None:
		user = Profile(
			rit_id = request.environ["uid"],
			first_name = request.environ["givenName"],
			last_name = request.environ["sn"],
			email = request.environ.get("email", request.environ.get("mail"))
		)

	return user
