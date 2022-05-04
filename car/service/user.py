import logging
from typing import List, Optional

from car.models import User, UserType
from car.utils.encrypt import Encryptor

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
    def get_list(
        cls,
        user_ids: Optional[List[int]] = None,
        names: Optional[List[str]] = None,
        types: Optional[List[UserType]] = None,
        platform_openids: Optional[List[str]] = None,
    ) -> List[User]:
        users = User.objects.all()
        if user_ids is not None:
            users = users.filter(id__in=user_ids)
        if names is not None:
            users = users.filter(name__in=names)
        if types is not None:
            users = users.filter(type__in=types)
        if platform_openids is not None:
            users = users.filter(platform_openid__in=platform_openids)
        return list(users)

    @classmethod
    def get_one(cls, user_id: int, assert_exist=True) -> Optional[User]:
        users = cls.get_list(user_ids=[user_id])
        if users:
            return users[0]
        else:
            if assert_exist:
                return users[0]
            else:
                return None

    @classmethod
    def exist(cls, user_id: int) -> bool:
        return bool(cls.get_list(user_ids=[user_id]))

    @classmethod
    def get_user_id(cls, session_id: str) -> Optional[int]:
        try:
            user_id = Encryptor.decrypt(session_id)
            return user_id
        except Exception as err:
            logging.error(err)
            return None

    @classmethod
    def gen_sessionid(cls, user_id: int) -> str:
        return Encryptor.encrypt(user_id)

    @classmethod
    def create(
        cls,
        name: str,
        phone: str,
        type: UserType,
        platform_openid: str,
        headimg: Optional[str] = None,
    ) -> User:
        user = User(
            name=name,
            phone=phone,
            headimg=headimg,
            type=type,
            platform_openid=platform_openid,
        )
        user.save()
        return user

    @classmethod
    def delete(cls, user_id: int) -> None:
        User.objects.get(id=user_id).delete()
