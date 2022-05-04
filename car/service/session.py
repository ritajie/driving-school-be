from typing import Optional, Tuple, Union

from car.models import Coach, User
from car.service.coach import CoachService
from car.service.user import UserService
from car.utils.encrypt import Encryptor


class SessionIDService:
    USER_PREFIX = 1
    COACH_PREFIX = -1

    @classmethod
    def gen_sessionid(cls, user_or_coach: Union[User, Coach]) -> str:
        prefix: int
        if isinstance(user_or_coach, User):
            prefix = cls.USER_PREFIX
        elif isinstance(user_or_coach, Coach):
            prefix = cls.COACH_PREFIX
        user_or_coach_id = user_or_coach.id
        return Encryptor.encrypt(user_or_coach_id * prefix)

    @classmethod
    def parse_sessionid(cls, sessionid: str) -> Tuple[Optional[User], Optional[Coach]]:
        id_with_prefix = Encryptor.decrypt(sessionid)
        is_user = id_with_prefix > 0
        is_coach = id_with_prefix < 0
        if is_user:
            user_id = id_with_prefix // cls.USER_PREFIX
            user = UserService.get_one(user_id=user_id, assert_exist=False)
            coach = None
        elif is_coach:
            coach_id = id_with_prefix // cls.COACH_PREFIX
            coach = CoachService.get_one(coach_id, assert_exist=False)
            user = None
        return user, coach
