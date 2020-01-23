from flask import render_template, request, redirect, url_for

from notifications_python_client.notifications import NotificationsAPIClient
from itsdangerous import URLSafeTimedSerializer

from track.functions.generate_path import *

from track.main import main


@main.route("/en/verify-account", methods=['GET', 'POST'])
@main.route("/fr/verify-account", methods=['GET', 'POST'])
def verify_account():
	prefix = request.path[1:3]
	if request.method == 'GET':
		return render_template(generate_path(prefix, "verify-account"))
	else:
		phone = request.form.get('mobile_input')
		# Create Token and send text  notification
		# response = notifications_client.send_sms_notification(
		#     phone_number='+1' + phone,
		#     template_id='Some ID',
		#     personalisation={
		#         'token':token
		#     }
		# )

		# Hide Mobile Number
		# i = 0
		# hidden_phone = ''
		# for char in phone:
		#     if char == '-':
		#         hidden_phone += char
		#     else:
		#         if i < 6:
		#             hidden_phone += '*'
		#         else:
		#             hidden_phone += char
		#         i += 1
		return redirect('/' + prefix + '/verify-account/mobile')


@main.route("/en/verify-account/mobile", methods=['GET', 'POST'])
@main.route("/fr/verify-account/mobile", methods=['GET', 'POST'])
def verify_account_mobile():
	prefix = request.path[1:3]
	phone = 'placeholder: ***-***-3333'
	return render_template(generate_path(prefix, "verify-mobile"), phone=phone)

