from django.core.management.base import BaseCommand
from django.db.transaction import atomic

from car.models import User, UserType
from car.service.coach import CoachService
from car.service.order import OrderService
from car.service.user import UserService


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Does not write to db, just prints the log.",
        )
        parser.add_argument("--user_id", type=int, required=True)
        parser.add_argument("--username", type=int, required=True)

    @atomic()
    def handle(self, *args, **options):
        dry_run = options["dry_run"]
        user_id = options["user_id"]
        username = options["username"]

        user = self.get_user(user_id=user_id, username=username)
        self.check_user_is_new(user)

        if not dry_run:
            CoachService.create(
                name=username,
                phone=user.phone,
                type=UserType.Wechat,
                platform_openid=user.platform_openid,
                headimg=user.headimg,
            )
            UserService.delete(user_id=user_id)

    @classmethod
    def get_user(cls, user_id: int, username: str) -> User:
        user = UserService.get_one(user_id=user_id, assert_exist=False)
        if not user or user.name != username:
            raise Exception("用户不存在")
        return user

    @classmethod
    def check_user_is_new(cls, user: User) -> None:
        orders = OrderService.get_list(user_id=user.id)
        if orders:
            raise Exception("用户有订单数据")
