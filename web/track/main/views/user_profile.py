from flask import render_template, request
from flask_login import current_user, login_required

from track.functions.generate_path import *
from track.functions.generate_user_data import generate_user_data

from track.main import main


@main.route("/en/user-profile")
@main.route("/fr/user-profile")
@login_required
def user_profile():
	prefix = request.path[1:3]
	return render_template(generate_path(prefix, 'user-profile'), **generate_user_data(current_user.user_email))
