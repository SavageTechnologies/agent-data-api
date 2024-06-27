import json

from django.shortcuts import render

from core.views import BaseView
from search.serpapi_utils import search_google_local, search_youtube


# Create your views here.

class GoogleSearchView(BaseView):
    requires_login = True

    def get(self, request, *args, **kwargs):
        query_extra = request.GET.get("query", None)
        query_city = request.GET.get("city", None)
        query_state = request.GET.get("state", None)
        query_country = request.GET.get("country", "United States")
        try:
            query_limit = int(request.GET.get("limit", 15))
        except Exception:
            query_limit = 15

        query_limit = min(100, max(1, query_limit))

        context = {
            "search_results": None,
            "query": query_extra,
            "city": query_city,
            "state": query_state,
            "country": query_country,
            "limit": query_limit,
            "export_data": "[]",
        }

        if query_extra is not None and len(query_extra) > 0:
            locations = []
            if query_city is not None and len(query_city) > 0:
                locations.append(query_city)
            if query_state is not None and len(query_state) > 0:
                locations.append(query_state)
            if query_country is not None and len(query_country) > 0:
                locations.append(query_country)
            location = ", ".join(locations)
            search_results = search_google_local(query_extra, location, query_limit)
            context["search_results"] = search_results
            csv_data = [['Title', 'Address', 'Phone', 'Website', 'Type', 'Rating', 'Reviews']]
            for result in search_results:
                csv_data.append([result['title'], result['address'], result['phone'], result['website'], result['type'], result['rating'], result['reviews']])
            context["export_data"] = json.dumps(csv_data)

        return render(request, "serpapi_search.html", context=context)


class YoutubeSearchView(BaseView):
    requires_login = True

    def get(self, request, *args, **kwargs):
        query_extra = request.GET.get("query", None)
        try:
            query_limit = int(request.GET.get("limit", 15))
        except Exception:
            query_limit = 15

        query_limit = min(100, max(1, query_limit))

        context = {
            "search_results": None,
            "query": query_extra,
            "limit": query_limit,
            "export_data": "[]",
        }

        if query_extra is not None and len(query_extra) > 0:
            search_results = search_youtube(query_extra, query_limit)
            context["search_results"] = search_results
            csv_data = [['Title', 'Link', 'Description', 'Thumbnail']]
            for result in search_results:
                csv_data.append([result['title'], result['link'], result['description'], result['thumbnail']])
            context["export_data"] = json.dumps(csv_data)

        return render(request, "youtube_search.html", context=context)

