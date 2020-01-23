from flask import render_template, request, redirect
from flask_login import login_required, logout_user

from track.functions.generate_path import *

from track.main import main


@main.route("/en/logout")
@main.route("/fr/logout")
@login_required
def logout():
	prefix = request.path[1:3]
	logout_user()
	return render_template(generate_path(prefix, 'logout'))
