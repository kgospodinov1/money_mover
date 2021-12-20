from flask import render_template, request, abort, Blueprint, redirect, url_for
from flask_login import login_user, login_required, logout_user
from pydantic import ValidationError

from users.data.login_form import LoginData
from users.services import user_service

blueprint = Blueprint('users', __name__, template_folder='templates')


@blueprint.route('/', methods=["GET"])
def login_get():
    return render_template("login.html")


@blueprint.route('/login', methods=["POST"])
def login_post():
    try:
        data = LoginData(**request.json)
        user = user_service.login(data.username, data.password)
        if not user:
            raise abort(404)

        login_user(user)

        return redirect(url_for('transfers.list_'))

    except ValidationError as e:
        return {"form_errors": e.json()}, 400


@blueprint.route('/logout', methods=["GET"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("users.login_get"))
