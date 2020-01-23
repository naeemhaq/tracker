from flask import request, render_template, Blueprint

from track.functions.generate_path import *
from track.main import main


@main.route("/en/organizations/")
@main.route("/fr/organisations/")
def organizations():
	prefix = request.path[1:3]
	return render_template(generate_path(prefix, "organizations"))
