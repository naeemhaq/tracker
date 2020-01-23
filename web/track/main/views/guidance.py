from flask import request, render_template

from track.main import main
from track.functions.generate_path import *


@main.route("/en/guidance/")
@main.route("/fr/directives/")
def guidance():
	prefix = request.path[1:3]
	return render_template(generate_path(prefix, "guidance"))
