from flask import request, render_template

from track.main import main
from track.functions.generate_path import *


@main.route("/en/help/")
@main.route("/fr/aide/")
def help():
	prefix = request.path[1:3]
	return render_template(generate_path(prefix, "help"))
