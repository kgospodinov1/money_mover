import flask
from flask import render_template, request, Blueprint, abort, redirect, url_for
from flask_login import login_required, current_user

from transfers.data.money_transfer import MoneyTransferPublicData
from transfers.data.note import AddNoteData
from transfers.services import transfer_service

blueprint = Blueprint('transfers', __name__, template_folder='templates')


# List
@blueprint.route('/', methods=["GET"])
@login_required
def list_():
    return render_template("list.html")


# Fetch
@blueprint.route('/fetch_transfers', methods=["GET"])
@login_required
def fetch_transfers():
    page = request.args.get('page', 1, type=int)

    return {
        "result": [MoneyTransferPublicData.from_orm(mt).dict()
                   for mt in transfer_service.get_transfers_paginated(10, page)]
    }


# Details
@blueprint.route('/<int:transfer_id>', methods=["GET"])
@login_required
def transfers_details(transfer_id: int):
    transfer = transfer_service.get_by_id(transfer_id)
    if not transfer:
        raise abort(404)

    return render_template("details.html", transfer=transfer)


@blueprint.route('/<int:transfer_id>/add_note', methods=["POST"])
@login_required
def add_note(transfer_id: int):
    try:
        data = AddNoteData(**request.form)
        transfer_service.add_note(transfer_id, data.note, current_user.get_id())
    except ValueError:
        flask.flash("Note cannot be empty", "error")

    return redirect(url_for("transfers.transfers_details",
                            transfer_id=transfer_id))
