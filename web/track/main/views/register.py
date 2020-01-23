from flask import current_app as app

from track.functions.generate_user_data import *
from track.functions.generate_path import *
from track.functions.input_validators import *
from track.functions.error_messages import *

from flask import render_template, request, redirect

from flask_login import current_user
from flask_bcrypt import Bcrypt

from track.main import main


@main.route("/en/register", methods=['GET', 'POST'])
@main.route("/fr/register", methods=['GET', 'POST'])
def register_user():
	prefix = request.path[1:3]
	bcrypt = Bcrypt(app)

	# User visiting register page, display page
	if request.method == 'GET':
		if current_user.is_authenticated:
			# If a user is already logged in, redirect to user-profile
			return redirect('user-profile', **generate_user_data(current_user.user_email))
		else:
			return render_template(generate_path(prefix, "register"))

	else:
		user_name = cleanse_input(request.form.get('name_input'))
		user_email = cleanse_input(request.form.get('email_input'))
		user_password = cleanse_input(request.form.get('password_input'))
		user_password_confirm = cleanse_input(request.form.get('password_confirm_input'))

		# Check if passwords match
		if user_password == user_password_confirm:
			if is_strong_password(user_password):

				user = connection.query_user_by_email(user_email)

				if user is not None:
					# User already exists using this email
					content = email_already_taken(user_name, user_email)
					return render_template(generate_path(prefix, "register"), **content)

				else:
					# Create a user to insert into the database
					to_add = Users(
						username=user_name,
						display_name=user_name,
						user_email=user_email.lower(),
						# Flask-BCrypt password hash
						user_password=bcrypt.generate_password_hash(user_password).decode('UTF-8'),
						preferred_lang="English",
						failed_login_attempts=0
					)
					connection.insert(to_add)
					connection.commit()

					return render_template(generate_path(prefix, "email-sent"))

			else:
				content = password_weak_register(user_name, user_email)
				return render_template(generate_path(prefix, "register"), **content)

		else:
			# If passwords do not match, redirect back to register page with appropriate error message.
			content = password_not_match_register(user_name, user_email)
			return render_template(generate_path(prefix, "register"), **content)
