from functools import wraps

from .db import Profile, db, commit

from flask import Request, abort
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
			email = request.environ.get("email", request.environ.get('mail'))
		)

	return user

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        org = kwargs.get('org')

        if org:
            if org not in [a.organization_id for a in flask_login.current_user.positions]:
                abort(403)
        else:
            if not flask_login.current_user.positions:
                abort(403)

        return f(*args, **kwargs)
    return decorated_function