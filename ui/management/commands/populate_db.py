# pylint: disable=imported-auth-user
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from ui.models import Assignment


class Command(BaseCommand):
    help = "Populate the DB with some initial data (an admin user and an assignment)"

    def handle(self, *args, **kwargs) -> None:
        user_count = User.objects.all().count()
        if user_count != 0:
            print("The DB is already populated")
            return

        User.objects.create_user(
            username="admin", email="admin@admin.com", password="admin", is_staff=True, is_superuser=True
        )

        Assignment.objects.create(
            gitlab_private_token="REPLACE_WITH_OWN_TOKEN",
            gitlab_project_id=-1,
            long_name="Long Name of Assignment",
            short_name="Short Name of Assignment",
            max_score=100,
        )
