from datetime import datetime

from .config import *
from .user_model import *

from track import models
from track.cache import cache


from flask import Flask, request, render_template
from http import HTTPStatus

from track.config import config
from track.functions.generate_path import generate_path
from track.cache import cache

import flask_login


def create_app(environment='default'):
    app = Flask(__name__, instance_relative_config=True)

    configuration = config.get(environment, 'default')
    app.config.from_object(configuration)
    configuration.init_app(app)

    app.config.from_pyfile('application.cfg', silent=True)

    from track.cache import cache
    cache.init_app(app)

    # from track import views
    # views.register(app)

    # Set Flask Login Information
    app.secret_key = os.getenv('SUPER_SECRET_KEY')
    login_manager = flask_login.LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def user_loader(user_id):
        return None

    # Import Views
    from track.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # Error Handlers
    register_error_handlers(app)

    from track import helpers
    helpers.register(app)

    from track.models import db
    db.init_app(app)

    return app


def register_error_handlers(app):
    # Every response back to the browser will include these web response headers
    @app.after_request
    def apply_headers(response):
        return response

    @app.errorhandler(404)
    def page_not_found(error):
        prefix = request.path[1:3]
        return render_template(generate_path(prefix, '404')), HTTPStatus.NOT_FOUND

    @app.errorhandler(401)
    def invalid_credentials(error):
        prefix = request.path[1:3]
        return render_template(generate_path(prefix, '401')), HTTPStatus.UNAUTHORIZED

    @app.errorhandler(models.QueryError)
    def handle_invalid_usage(error):
        app.logger.error(error)
        return render_template("404.html"), HTTPStatus.NOT_FOUND

    @app.before_request
    def verify_cache():
        cur_time = datetime.now()

        if cache.get('last-cache-bump') is None:
            cache.set('last-cache-bump', cur_time)

        if cache.get('cache-timer') is None:
            # Set up a 5 minute timer to minimize flailing.
            cache.set('cache-timer', cur_time, 5 * 60)

            # Let's check the remote cache flag (time value)
            remote_signal = datetime.strptime(models.Flag.get_cache(), "%Y-%m-%d %H:%M")
            app.logger.warn("TRACK_CACHE: remote signal @ {}".format(remote_signal))

            if remote_signal is not None:
                if cache.get('last-cache-bump') < remote_signal:
                    app.logger.warn("TRACK_CACHE: Cache reset @ {} due to signal @ {}".format(cur_time, remote_signal))
                    cache.clear()
                    # We've blown the whole cache, so reset the cache timer, and the remote val.
                    cache.set('cache-timer', cur_time, 5 * 60)
                    cache.set('last-cache-bump', remote_signal)
            else:
                app.logger.error("TRACK_CACHE: remote cache datetime was None. Danger Will Robinson.")
