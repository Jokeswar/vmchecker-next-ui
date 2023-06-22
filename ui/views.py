import base64
import logging

from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpRequest, HttpResponse, HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from ui.core.api.vmck_api import VMCheckerAPI
from ui.forms.gitlab_retrieve_form import GitlabRetriveForm
from ui.forms.login_form import LoginForm
from ui.forms.upload_form import UploadFileForm
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

        if "submitFromGitlab" in request.POST:
            retrieve_form = GitlabRetriveForm(request.POST)
            if retrieve_form.is_valid():
                gitlab_project_id = int(retrieve_form.data["gitlab_project_id"])
                gitlab_private_token = retrieve_form.data["gitlab_private_token"]
                gitlab_branch = retrieve_form.data["gitlab_branch"]

                api = VMCheckerAPI(settings.VMCK_BACKEND_URL)
                archive = api.retrive_archive(gitlab_private_token, gitlab_project_id, gitlab_branch)
                uuid = api.submit(
                    assignment.gitlab_private_token,
                    assignment.gitlab_project_id,
                    assignment.gitlab_branch,
                    request.user.username,
                    archive,
                )
                Submission.objects.create(user=request.user, assignment=assignment, evaluator_job_id=uuid)
        elif "submitYourArchive" in request.POST:
            upload_form = UploadFileForm(request.POST, request.FILES)
            if upload_form.is_valid():
                file = request.FILES["file"]
                api = VMCheckerAPI(settings.VMCK_BACKEND_URL)
                uuid = api.submit(
                    assignment.gitlab_private_token,
                    assignment.gitlab_project_id,
                    assignment.gitlab_branch,
                    request.user.username,
                    str(base64.encodebytes(file.read()), encoding="ascii"),
                )
                Submission.objects.create(user=request.user, assignment=assignment, evaluator_job_id=uuid)

    retrieve_form = GitlabRetriveForm()
    upload_form = UploadFileForm()

    return render(
        request,
        "ui/assignment.html",
        {
            "assignment": assignment,
            "submissions": page_submissions,
            "retrieve_form": retrieve_form,
            "upload_form": upload_form,
        },
    )


@login_required
def submission_result(request: HttpRequest, pk: int) -> HttpResponse:
    sub = get_object_or_404(Submission, pk=pk)

    if sub.user.pk != request.user.pk:
        return HttpResponseForbidden()

    api = VMCheckerAPI(settings.VMCK_BACKEND_URL)

    trace = api.trace(sub.evaluator_job_id)
    trace_start_marker = trace.find("<VMCK_NEXT_BEGIN>")
    trace_start_position = trace_start_marker + len("<VMCK_NEXT_BEGIN>") + 1 if trace_start_marker > 0 else 0
    trace = trace[trace_start_position:]

    trace_end_marker = trace.find("<VMCK_NEXT_END>")
    trace_end_position = trace_end_marker if trace_start_marker > 0 else -1
    trace = trace[:trace_end_position]

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
