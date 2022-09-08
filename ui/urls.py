from django.contrib import admin
from django.urls import path

from ui import views

urlpatterns = [
    path("", views.landing_page),
    path("login", views.login_page),
    path("logout", views.logout_page),
    path("homepage", views.homepage),
    path("assignment/<int:pk>", views.assignment_mainpage, name=views.assignment_mainpage.__name__),
    path("admin/", admin.site.urls),
    path("health", views.health),
]
