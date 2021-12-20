import sqlalchemy as sa
from sqlalchemy.orm import relationship

from common.db import Base


class User(Base):
    __tablename__ = "users"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    username: str = sa.Column(sa.String, unique=True, nullable=False,
                              index=True)
    password: str = sa.Column(sa.String, nullable=False)
    wallets = relationship("Wallet", back_populates="owner")
    is_staff: bool = sa.Column(sa.Boolean, default=False, nullable=False)
    is_active: bool = sa.Column(sa.Boolean, default=False, nullable=False)

    def get_id(self):
        return self.id

    def is_authenticated(self):
        return self.is_staff and self.is_staff

    def is_anonymous(self):
        return not self.is_staff
