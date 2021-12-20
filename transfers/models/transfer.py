import datetime
from decimal import Decimal

import sqlalchemy as sa
from sqlalchemy.orm import relationship

from common.db import Base
from transfers.enums import MoneyTransferStatusEnum
from users.models.user import User


class Currency(Base):
    __tablename__ = "currencies"
    name: str = sa.Column(sa.String, primary_key=True, autoincrement=False)


class MoneyTransfer(Base):
    __tablename__ = "money_transfers"
    id: int = sa.Column(sa.Integer, primary_key=True, autoincrement=True)

    originator_id: int = sa.Column(
        sa.Integer, sa.ForeignKey('users.id'), nullable=False)
    receiver_id: int = sa.Column(
        sa.Integer, sa.ForeignKey('users.id'), nullable=False)

    date_modified: datetime.datetime = sa.Column(
        sa.DateTime, onupdate=datetime.datetime.utcnow, nullable=False,
        index=True)
    amount: Decimal = sa.Column(sa.Numeric(precision=12, scale=2),
                                nullable=False)
    currency: str = sa.Column(sa.String, sa.ForeignKey('currencies.name'))
    status: int = sa.Column(sa.Integer, nullable=False)

    originator: User = relationship("User", backref="outgoing_transfers",
                                    foreign_keys=[originator_id])
    receiver: User = relationship("User", backref="incoming_transfers",
                                  foreign_keys=[receiver_id])
    notes: User = relationship("MoneyTransferStaffNote", backref="transfer",
                               order_by="desc(MoneyTransferStaffNote.date_created)")

    def get_status_display(self) -> str:
        return MoneyTransferStatusEnum(self.status).name


class MoneyTransferStaffNote(Base):
    __tablename__ = "money_transfers_staff_notes"
    id: int = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    created_by_id: int = sa.Column(sa.Integer, sa.ForeignKey('users.id'),
                                   nullable=False)
    money_transfer_id: int = sa.Column(
        sa.Integer, sa.ForeignKey('money_transfers.id'), nullable=False)
    date_created: datetime.datetime = sa.Column(sa.DateTime,
                                                default=datetime.datetime.utcnow,
                                                nullable=False)
    note: str = sa.Column(sa.Text, nullable=False)

    created_by: User = relationship("User", backref="notes")
