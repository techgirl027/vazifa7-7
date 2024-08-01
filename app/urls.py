from app.views import *
from django.urls import path, include
from app import views

# from . import views


urlpatterns = [
    path("", views.home_page, name="home"),
    path("register/", register_page, name="register"),
    path("authentication/", include("app.authentication.urls")),
    path("back-office/", include("app.back-office.urls")),
    path("user/", include("app.user.urls")),
]
