import os

from http import HTTPStatus

from flask import abort


def generate_path(prefix, page_id):
	if prefix == "en" or prefix == "fr":
		return os.path.join(prefix, "{}.html".format(page_id))
	else:
		abort(HTTPStatus.NOT_FOUND)