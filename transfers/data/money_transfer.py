from pydantic_sqlalchemy import sqlalchemy_to_pydantic

from transfers.models.transfer import MoneyTransfer
from users.data.user import UserPublicData

MoneyTransferData = sqlalchemy_to_pydantic(MoneyTransfer)


class MoneyTransferPublicData(MoneyTransferData):
    originator: UserPublicData
    receiver: UserPublicData
