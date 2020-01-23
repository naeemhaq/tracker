from flask import Blueprint

main = Blueprint('main', __name__)

from track.main.views import (
	cache_buster,
	data,
	domians,
	forgot_password,
	guidance,
	help,
	index,
	new_password,
	organizations,
	password_changed,
	register,
	sign_in,
	sign_out,
	user_profile,
	verify_account
)
