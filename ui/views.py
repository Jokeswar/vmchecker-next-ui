import logging
import re

from django.utils import timezone
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpRequest, HttpResponse, JsonResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render

from ui.core.api.vmck_api import VMCheckerAPI
from ui.forms.gitlab_retrieve_form import GitlabRetriveForm
from ui.forms.login_form import LoginForm
from ui.models import Assignment, Submission

LOG = logging.getLogger(__file__)


def landing_page(request: HttpRequest) -> HttpResponse:
    return redirect(homepage) if request.user.is_authenticated else redirect(login_page)


def login_page(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        return redirect(homepage)

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.data["username"]
            password = form.data["password"]

            if not (user := authenticate(username=username, password=password)):
                LOG.info("Login failure for username: %s", username)
            else:
                login(request, user)
                return redirect(homepage)
    else:
        form = LoginForm()

    return render(request, "ui/login.html", {"form": form})


def logout_page(request: HttpRequest) -> HttpResponse:
    logout(request)
    return redirect(landing_page)


@login_required
def homepage(request: HttpRequest) -> HttpResponse:
    return render(
        request,
        "ui/homepage.html",
        {"assignments": Assignment.objects.all()},
    )


@login_required
def assignment_mainpage(request: HttpRequest, pk: int) -> HttpResponse:
    assignment = get_object_or_404(Assignment, pk=pk)
    submissions = Submission.objects.all().order_by("-id").select_related("assignment")

    paginator = Paginator(submissions, settings.PAGINATION_SIZE)
    page = request.GET.get("page", "1")
    page_submissions = paginator.get_page(page)

    if request.method == "POST":
        if assignment.deadline_hard and timezone.now() > assignment.deadline_hard:
            return HttpResponseForbidden("You tried to submit after the hard deadline!")

        retrieve_from = GitlabRetriveForm(request.POST)
        if retrieve_from.is_valid():
            gitlab_project_id = int(retrieve_from.data["gitlab_project_id"])
            gitlab_private_token = retrieve_from.data["gitlab_private_token"]

            api = VMCheckerAPI(settings.VMCK_BACKEND_URL)
            archive = api.retrive_archive(gitlab_private_token, gitlab_project_id)
            uuid = api.submit(
                assignment.gitlab_private_token, assignment.gitlab_project_id, request.user.username, archive
            )
            Submission.objects.create(user=request.user, assignment=assignment, evaluator_job_id=uuid)

    else:
        retrieve_from = GitlabRetriveForm()

    return render(
        request,
        "ui/assignment.html",
        {
            "assignment": assignment,
            "submissions": page_submissions,
            "retrieve_form": retrieve_from,
        },
    )


@login_required
def submission_result(request: HttpRequest, pk: int) -> HttpResponse:
    sub = get_object_or_404(Submission, pk=pk)

    if sub.user.pk != request.user.pk:
        return HttpResponseForbidden()

    api = VMCheckerAPI(settings.VMCK_BACKEND_URL)

    trace = api.trace(sub.evaluator_job_id)
    trace = trace[trace.find("VMCHECKER_TRACE_CLEANUP") + len("VMCHECKER_TRACE_CLEANUP") + 1 :]
    score_line = re.findall(r".*Total:\s*\d+\/\d+(?:.\d+)?", trace)[0]
    trace = trace[: trace.find(score_line) + len(score_line)]

    return render(
        request,
        "ui/submission_result.html",
        {
            "sub": sub,
            "sub_trace": trace,
            "submission_assignment": {
                "text": sub.assignment.short_name,
                "pk": sub.assignment.pk,
            },
        },
    )


def health(_: HttpRequest) -> HttpResponse:
    return JsonResponse({"alive": True})
