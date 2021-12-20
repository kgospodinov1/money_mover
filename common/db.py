from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///database.db', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


# noinspection PyUnresolvedReferences
def init_models():
    from users.models.user import User
    from wallet.models.wallet import Wallet, WalletTransactions
    from transfers.models.transfer import MoneyTransfer
