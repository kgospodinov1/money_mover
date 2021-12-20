from flask import Flask, redirect, url_for
from flask_login import LoginManager

import settings
from common.db import db_session, init_models
from users.services import user_service

app = Flask(__name__)
app.secret_key = settings.SECRET_KEY


@app.route('/')
def entry():
    return redirect(url_for('users.login_get'))


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


def register_blueprints():
    from users.views import blueprint as users_blueprint
    from transfers.views import blueprint as transfers_blueprint

    # Users
    app.register_blueprint(users_blueprint, url_prefix='/users')
    # Transfers
    app.register_blueprint(transfers_blueprint, url_prefix='/transfers')


def setup_auth():
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "users.login_get"
    login_manager.user_loader(user_service.get_user_by_id)
    login_manager.id_attribute = "get_id"


def main():
    init_models()
    register_blueprints()
    setup_auth()
    app.run(debug=True)


if __name__ == "__main__":
    main()
