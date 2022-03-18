import logging
from typing import Optional

from car.models import User
from car.utils.encrypt import ResultIdConverter

NULL_USER = User(
    id=0,
    name="",
    phone="",
    headimg="",
    created_at=None,
    updated_at=None,
)


class UserService:
    @classmethod
    def get_one(cls, user_id: str) -> User:
        return User.objects.get(id=user_id)

    @classmethod
    def exist(cls, user_id: int) -> bool:
        return User.objects.filter(id=user_id).exists()

    @classmethod
    def get_user_id(cls, session_id: str) -> Optional[int]:
        try:
            user_id = ResultIdConverter.decrypt(session_id)
            return user_id
        except Exception as err:
            logging.error(err)
            return None

    @classmethod
    def gen_sessionid(cls, user_id: int) -> str:
        return ResultIdConverter.encrypt(user_id)

    @classmethod
    def create(
        cls,
        name: str,
        phone: str,
        headimg: Optional[str] = None,
    ) -> User:
        user = User(
            name=name,
            phone=phone,
            headimg=headimg,
        )
        user.save()
        return user
