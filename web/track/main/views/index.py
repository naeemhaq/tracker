import os
from http import HTTPStatus

from flask import render_template, request, redirect

from track.functions.generate_path import *
from track.main import main


@main.route("/")
def index():
	user_lang = request.headers.get("Accept-Language", "en")
	if user_lang[:2] == "fr":
		return redirect("/fr/index/")
	else:
		return redirect("/en/index/")


@main.route("/en/")
@main.route("/fr/")
@main.route("/en/index/")
@main.route("/fr/index/")
def splash_page():
	prefix = request.path[1:3]
	return render_template(generate_path(prefix, "index"))
