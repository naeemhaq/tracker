import os

from track.config import *
from track.user_model import *

from flask import url_for

from itsdangerous import URLSafeTimedSerializer
from notifications_python_client.notifications import NotificationsAPIClient

NOTIFICATION_API_KEY = os.getenv('NOTIFICATION_API_KEY')
NOTIFICATION_API_URL = os.getenv('NOTIFICATION_API_URL')
SUPER_SECRET_KEY = os.getenv('SUPER_SECRET_KEY')
SUPER_SECRET_SALT = os.getenv('SUPER_SECRET_SALT')

notifications_client = NotificationsAPIClient(
	NOTIFICATION_API_KEY,
	NOTIFICATION_API_URL,
)


def send_pass_reset(user, prefix, template_id):
	password_reset_serial = URLSafeTimedSerializer(SUPER_SECRET_KEY)
	password_reset_url = url_for('main.' + prefix + '_new_password',
								 token=password_reset_serial.dumps(user.user_email, salt=SUPER_SECRET_SALT),
								 _external=True
								 )
	response = notifications_client.send_email_notification(
		email_address=user.user_email,
		personalisation={
			'user': user.display_name,
			'password_reset_url': password_reset_url
		},
		template_id=template_id
	)
