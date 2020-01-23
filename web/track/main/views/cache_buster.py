from http import HTTPStatus

from track.cache import cache
from track.main import main


@main.route("/data/cache-buster")
def cache_bust():
	try:
		cache.clear()
		return "", HTTPStatus.NO_CONTENT
	except Exception as exc:
		return str(exc), HTTPStatus.INTERNAL_SERVER_ERROR
