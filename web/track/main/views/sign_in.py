import os

from flask import current_app as app
from flask import render_template, request, redirect
from flask_login import login_user, current_user
from flask_bcrypt import Bcrypt

from track.functions.email_templates import *
from track.functions.error_messages import *
from track.functions.generate_path import *
from track.functions.input_validators import *
from track.functions.send_pass_reset import *
from track.functions.generate_user_data import generate_user_data

from track.main import main
from track.user_model import *

DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')
SUPER_SECRET_KEY = os.getenv('SUPER_SECRET_KEY')

connection = Connection(_user=DB_USER, _password=DB_PASS, _host=DB_HOST, _port=DB_PORT, _db=DB_NAME)


@main.route("/en/sign-in", endpoint='en_sign_in', methods=['GET', 'POST'])
@main.route("/fr/sign-in", endpoint='fr_sign_in', methods=['GET', 'POST'])
def sign_in_page():
	prefix = request.path[1:3]
	bcrypt = Bcrypt(app)

	if request.method == 'GET':
		if current_user.is_authenticated:
			# If a user is already logged in, redirect to user-profile
			return redirect('user-profile')
		else:
			return render_template(generate_path(prefix, "sign-in"))

	else:
		user_email = cleanse_input(request.form.get('email_input'))
		user_password = cleanse_input(request.form.get('password_input'))

		user = connection.query_user_by_email(user_email)

		if user is not None:  # If a user with that email address exists
			if not connection.is_user_account_locked(user_email):  # Check that account is not locked
				if bcrypt.check_password_hash(user.user_password, user_password):
					login_user(user)
					# After a successful login, set failed login attempts to 0
					connection.reset_failed_login_attempts(user_email)
					connection.commit()
					return redirect(url_for(generate_path(prefix, 'user-profile')), **generate_user_data(user_email))

				else:
					# If login fails, increment the failed attempts counter.
					connection.increment_failed_login_attempts(user_email)
					connection.commit()
			else:
				# This account is locked due to too many failed login attempts
				send_pass_reset(user, prefix, template_id=reset_locked_account_password_template())

				msg = 'Your account has been locked because you have exceeded' \
					  ' the maximum failed login attempts limit. Please check your' \
					  ' email for instructions on how to reset your password'

				return render_template(generate_path(prefix, "forgot-password"), msg=msg)

		# The sign in credentials were not valid, display appropriate error to the user.
		content = sign_in_incorrect(user_email)
		return render_template(generate_path(prefix, "sign-in"), **content)
