import datetime
import enum

import sqlalchemy as sa
from sqlalchemy.orm import relationship

from common.db import Base


class Wallet(Base):
    __tablename__ = "wallets"
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    owner_id = sa.Column(sa.Integer, sa.ForeignKey('users.id'))

    owner = relationship("User", back_populates="wallets")
    transactions = relationship("WalletTransactions", backref="wallet")


class WalletTransactionEnum(enum.Enum):
    DEBIT = 1
    CREDIT = 2


class WalletTransactions(Base):
    __tablename__ = "wallets_transactions"
    id: int = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    wallet_id: int = sa.Column(sa.Integer, sa.ForeignKey('wallets.id'))
    type: WalletTransactionEnum = sa.Column(sa.Integer)
    amount = sa.Column(sa.Numeric(precision=12, scale=2))
    currency: str = sa.Column(sa.String, sa.ForeignKey('currencies.name'))
    date_created: datetime.datetime = sa.Column(sa.DateTime,
                                                default=datetime.datetime.utcnow,
                                                nullable=False, index=True)
