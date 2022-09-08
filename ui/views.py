import logging

from django.conf import settings
from django.shortcuts import redirect, render, get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse, JsonResponse, HttpRequest
from ui.core.api.vmck_api import VMCheckerAPI

from ui.models import Assignment, Submission
from ui.forms.login_form import LoginForm
from ui.forms.gitlab_retrieve_form import GitlabRetriveForm

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

            user = authenticate(username=username, password=password)

            if not user:
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

    paginator = Paginator(submissions, 25)
    page = request.GET.get("page", "1")
    page_submissions = paginator.get_page(page)

    if request.method == "POST":
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
        {"assignment": assignment, "submissions": page_submissions, "retrieve_form": retrieve_from},
    )


def health(_: HttpRequest) -> HttpResponse:
    return JsonResponse({"alive": True})
