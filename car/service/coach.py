from typing import List, Optional

from car.models import Coach, UserType


class CoachService:
    @classmethod
    def get_list(
        cls,
        coach_ids: Optional[List[int]] = None,
        names: Optional[List[str]] = None,
        types: Optional[List[UserType]] = None,
        platform_openids: Optional[List[str]] = None,
    ) -> List[Coach]:
        coachs = Coach.objects.all()
        if coach_ids is not None:
            coachs = coachs.filter(id__in=coach_ids)
        if names is not None:
            coachs = coachs.filter(name__in=names)
        if types is not None:
            coachs = coachs.filter(type__in=types)
        if platform_openids is not None:
            coachs = coachs.filter(platform_openid__in=platform_openids)
        return list(coachs)

    @classmethod
    def get_one(cls, coach_id: int, assert_exist=True) -> Coach:
        coachs = cls.get_list(coach_ids=[coach_id])
        if coachs:
            return coachs[0]
        else:
            if assert_exist:
                return coachs[0]
            else:
                return None

    @classmethod
    def create(
        cls,
        name: str,
        phone: str,
        type: UserType,
        platform_openid: str,
        headimg: Optional[str] = None,
    ) -> Coach:
        coach = Coach(
            name=name,
            phone=phone,
            headimg=headimg,
            type=type,
            platform_openid=platform_openid,
        )
        coach.save()
        return coach
