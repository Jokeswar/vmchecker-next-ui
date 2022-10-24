# pylint: disable=imported-auth-user
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models

from ui.core.api.vmck_api import VMCheckerAPI


class Assignment(models.Model):
    gitlab_private_token = models.CharField(max_length=40, blank=False, null=False)
    gitlab_project_id = models.BigIntegerField(blank=False, null=False)
    long_name = models.CharField(max_length=256, blank=False, null=False)
    short_name = models.CharField(max_length=64, blank=False, null=False)
    description = models.TextField(blank=True, null=True)

    max_score = models.DecimalField(max_digits=5, decimal_places=2, blank=False, null=False)
    deadline_soft = models.DateTimeField(blank=True, null=True)
    deadline_hard = models.DateTimeField(blank=True, null=True)


class Feedback(models.Model):
    reviewer = models.ForeignKey(User, on_delete=models.PROTECT, null=True)
    feedback = models.TextField(null=True)


class Submission(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, blank=False, null=False)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, blank=False, null=False)
    feedback = models.ForeignKey(Feedback, on_delete=models.CASCADE, blank=True, null=True)
    evaluator_job_id = models.CharField(max_length=36, blank=False, null=False)

    score = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)

    @property
    def get_state_display(self) -> str:
        api = VMCheckerAPI(settings.VMCK_BACKEND_URL)
        status = api.status(self.evaluator_job_id)
        return str(status.name)

    def __str__(self):
        return f"Submission#{self.pk} by {self.user}"
