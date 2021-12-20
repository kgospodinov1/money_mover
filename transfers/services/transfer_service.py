from typing import List, Optional
from flask import escape

from common.db import db_session
from transfers.models.transfer import MoneyTransfer, MoneyTransferStaffNote


def get_transfers_paginated(per_page: int, page: int) -> List[MoneyTransfer]:
    if page < 1:
        page = 1

    if per_page < 1:
        per_page = 1

    page -= 1
    return MoneyTransfer.query\
        .order_by(MoneyTransfer.date_modified.desc())\
        .offset(page*per_page)\
        .limit(per_page)\
        .all()


def get_by_id(_id: int) -> Optional[MoneyTransfer]:
    return MoneyTransfer.query.filter(MoneyTransfer.id == _id).first()


def add_note(transfer_id: int, note: str, created_by_id: int) -> None:
    note = escape(note)
    note_o = MoneyTransferStaffNote(
        created_by_id=created_by_id,
        money_transfer_id=transfer_id,
        note=note
    )
    db_session.add(note_o)
    db_session.commit()
