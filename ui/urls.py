from django.contrib import admin
from django.urls import path

from ui import views

urlpatterns = [
    path("", views.landing_page),
    path("login", views.login_page, name=views.login_page.__name__),
    path("logout", views.logout_page, name=views.logout_page.__name__),
    path("homepage", views.homepage, name=views.homepage.__name__),
    path("assignment/<int:pk>", views.assignment_mainpage, name=views.assignment_mainpage.__name__),
    path("submission/<int:pk>", views.submission_result, name=views.submission_result.__name__),
    path("admin/", admin.site.urls),
    path("health", views.health),
]
