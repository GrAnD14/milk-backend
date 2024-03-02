from django.core.management import BaseCommand

from app.models import CustomUser


def add_users():
    CustomUser.objects.create_user("user", "user@user.com", "1234")
    CustomUser.objects.create_superuser("root", "root@root.com", "1234")

    for i in range(2, 3):
        CustomUser.objects.create_user(f"user{i}", f"user{i}@user.com", "1234")
        CustomUser.objects.create_superuser(f"root{i}", f"root{i}@root.com", "1234")

    print("Пользователи созданы")


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        add_users()

