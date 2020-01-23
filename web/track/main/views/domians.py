from flask import request, render_template

from track.main import main
from track.functions.generate_path import *


@main.route("/en/domains/")
@main.route("/fr/domaines/")
def https_domains():
	prefix = request.path[1:3]
	return render_template(generate_path(prefix, "domains"))
