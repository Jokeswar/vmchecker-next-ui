from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from ui.models import Assignment


class Command(BaseCommand):
    help = "Displays current time"

    def handle(self, *args, **kwargs) -> None:
        User.objects.create_user(
            username="admin", email="admin@admin.com", password="admin", is_staff=True, is_superuser=True
        )

        Assignment.objects.create(
            gitlab_private_token="REPLACE_WITH_OWN_TOKEN",
            gitlab_project_id=-1,
            long_name="Long Name of Assignment",
            short_name="ShortName",
            max_score=100,
        )
