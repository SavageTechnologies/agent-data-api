from django.urls import path

from user.views import LoginView, LogoutView

site_urls = [
    path("login/", LoginView.as_view()),
    path("logout/", LogoutView.as_view()),
]