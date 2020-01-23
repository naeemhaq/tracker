from flask import current_app as app
from flask import render_template, request
from flask_login import login_required, logout_user

from track.functions.email_templates import *
from track.functions.generate_path import *
from track.functions.input_validators import *
from track.functions.send_pass_reset import *

from track.main import main

DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')
SUPER_SECRET_KEY = os.getenv('SUPER_SECRET_KEY')

connection = Connection(_user=DB_USER, _password=DB_PASS, _host=DB_HOST, _port=DB_PORT, _db=DB_NAME)


@main.route("/en/forgot-password", methods=['GET', 'POST'])
@main.route("/fr/forgot-password", methods=['GET', 'POST'])
def forgot_password():
	prefix = request.path[1:3]
	if request.method == 'GET':
		return render_template(generate_path(prefix, "forgot-password"))
	else:

		user_email = cleanse_input(request.form.get('email_input'))
		user = connection.query_user_by_email(user_email)

		if user is not None and user.is_authenticated:
			send_pass_reset(user, prefix, template_id=reset_forgotten_password_template())

		msg = 'If an account is associated with the email address, ' \
			  'further instructions will arrive in your inbox'
		return render_template(generate_path(prefix, "forgot-password"), msg=msg)
