from django.contrib import admin

from ui.models import Assignment, Submission


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = [
        "short_name",
        "long_name",
        "max_score",
        "deadline_soft",
        "deadline_hard",
    ]


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    pass
