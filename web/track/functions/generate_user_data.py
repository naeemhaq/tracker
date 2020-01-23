import os

from track.user_model import *

DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')

connection = Connection(_user=DB_USER, _password=DB_PASS, _host=DB_HOST, _port=DB_PORT, _db=DB_NAME)


def generate_user_data(_email):
	user = connection.query_user_by_email(_email)
	return {
		'id': user.id,
		'username': user.username,
		'display_name': user.display_name,
		'user_email': user.user_email,
		# 'user_password': user.user_password,
		'preferred_lang': user.preferred_lang
		# 'failed_login_attempts': user.failed_login_attempts
}