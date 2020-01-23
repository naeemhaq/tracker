from flask import current_app as app
from flask import render_template, request, redirect
from flask_bcrypt import Bcrypt

from track.functions.error_messages import *
from track.functions.generate_path import *
from track.functions.input_validators import *
from track.functions.send_pass_reset import *

from track.main import main
from track.user_model import *

DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')
SUPER_SECRET_KEY = os.getenv('SUPER_SECRET_KEY')

connection = Connection(_user=DB_USER, _password=DB_PASS, _host=DB_HOST, _port=DB_PORT, _db=DB_NAME)


@main.route("/en/new-password/<token>", endpoint='en_new_password', methods=['GET', 'POST'])
@main.route("/fr/new-password/<token>", endpoint='fr_new_password', methods=['GET', 'POST'])
def new_password(token):
	prefix = request.path[1:3]
	bcrypt = Bcrypt(app)

	if request.method == 'GET':
		return render_template(generate_path(prefix, 'new-password'), token=token)
	else:
		# Try to see if email matches email set in token
		try:
			password_reset_serial = URLSafeTimedSerializer(SUPER_SECRET_KEY)
			email = password_reset_serial.loads(token, salt=SUPER_SECRET_SALT, max_age=3600)
		except:
			content = sign_in_change_pass()
			return redirect(url_for(prefix + '_sign_in', **content))

		user = connection.query_user_by_email(email)

		user_password = cleanse_input(request.form.get('password_input'))
		user_password_confirm = cleanse_input(request.form.get('password_confirm_input'))

		if user_password == user_password_confirm:
			if is_strong_password(user_password):
				# Create a user to insert into the database
				# Flask-BCrypt password hash
				user_password = bcrypt.generate_password_hash(user_password).decode('UTF-8')

				result = connection.update_user_password(email, user_password)

				if result:
					# A new password resets this account's failed login attempts
					connection.reset_failed_login_attempts(user.user_email)
					return render_template(generate_path(prefix, "password-changed"))
				else:
					content = password_db_error(token)
					return render_template(generate_path(prefix, "new-password"), **content)
			else:
				content = password_weak_forgot(token)
				return render_template(generate_path(prefix, "new-password"), **content)

		else:
			content = password_no_match_forgot(token)
			return render_template(generate_path(prefix, "new-password"), **content)
