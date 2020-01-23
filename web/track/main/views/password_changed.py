from flask import render_template, request
from track.functions.generate_path import *

from track.main import main


@main.route("/en/password-changed")
@main.route("/fr/password-changed")
def password_changed():
	prefix = request.path[1:3]
	return render_template(generate_path(prefix, 'password-changed'))
