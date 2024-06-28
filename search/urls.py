from django.urls import path

from search.views import GoogleSearchView, YoutubeSearchView, LocalGoogleSearchApiView, YoutubeSearchApiView

site_urls = [
    path("google/", GoogleSearchView.as_view()),
    path("youtube/", YoutubeSearchView.as_view()),
]
api_urls = [
    path("google/", LocalGoogleSearchApiView.as_view()),
    path("youtube/", YoutubeSearchApiView.as_view()),
]