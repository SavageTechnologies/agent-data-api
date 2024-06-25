from django.urls import path

from search.views import GoogleSearchView

site_urls = [
    path("google/", GoogleSearchView.as_view()),
]