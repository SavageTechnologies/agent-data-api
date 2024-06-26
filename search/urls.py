from django.urls import path

from search.views import GoogleSearchView, YoutubeSearchView

site_urls = [
    path("google/", GoogleSearchView.as_view()),
    path("youtube/", YoutubeSearchView.as_view()),
]