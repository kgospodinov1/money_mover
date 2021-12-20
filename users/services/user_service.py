from typing import Optional

import bcrypt as bcrypt

from users.models.user import User


def login(username: str, password: str) -> Optional[User]:
    user = User.query.filter(
        User.username == username,
        User.is_staff == True,
        User.is_active == True
    ).first()

    if not user:
        return None

    if not verify_hash(password, user.password):
        return None

    return user


def hash_password(password: str) -> str:
    hashed_text = bcrypt.hashpw(password.encode("utf8"), bcrypt.gensalt(10))
    return hashed_text.decode("utf8")


def verify_hash(password: str, hashed_password: str) -> bool:
    password = password.encode("utf8")
    hashed_password = hashed_password.encode("utf8")
    return bcrypt.checkpw(password, hashed_password)


def get_user_by_id(user_id: int) -> Optional[User]:
    return User.query.filter(User.id == user_id).first()
