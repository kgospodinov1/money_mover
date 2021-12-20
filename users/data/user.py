from pydantic_sqlalchemy import sqlalchemy_to_pydantic

from users.models.user import User

UserPublicData = sqlalchemy_to_pydantic(User, exclude=["wallets",
                                                       "password", "is_staff"])