import json

from django.http import JsonResponse
from django.shortcuts import render

from core.errors import ServerException
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

        context = {
            "search_results": None,
            "query": query_extra,
            "city": query_city,
            "state": query_state,
            "country": query_country,
        }

        return render(request, "serpapi_search.html", context=context)


class LocalGoogleSearchApiView(BaseView):
    requires_login = True

    def get(self, request, *args, **kwargs):
        query_extra = request.GET.get("query", None)
        query_city = request.GET.get("city", None)
        query_state = request.GET.get("state", None)
        query_next_id = request.GET.get("next", None)
        query_country = request.GET.get("country", "United States")
        try:
            query_next_id = int(query_next_id)
        except Exception:
            query_next_id = 0

        locations = []
        if query_city is not None and len(query_city) > 0:
            locations.append(query_city)
        if query_state is not None and len(query_state) > 0:
            locations.append(query_state)
        if query_country is not None and len(query_country) > 0:
            locations.append(query_country)
        location = ", ".join(locations)
        search_results = search_google_local(query_extra, location, query_next_id)
        results = []
        for r in search_results:
            results.append({
                "title": r["title"],
                "address": r["address"],
                "phone": r["phone"],
                "website": r["website"],
                "type": r["type"],
                "rating": r["rating"],
                "reviews": r["reviews"],
            })

        next_value = query_next_id + len(results)
        if len(results) < 20:
            next_value = None

        json_results = {
            "results": results,
            "next": next_value,
        }
        return JsonResponse(
            data=json_results
        )


class YoutubeSearchView(BaseView):
    requires_login = True

    def get(self, request, *args, **kwargs):
        query_extra = request.GET.get("query", None)
        context = {
            "search_results": None,
            "query": query_extra,
        }

        return render(request, "youtube_search.html", context=context)


class YoutubeSearchApiView(BaseView):
    requires_login = True

    def get(self, request, *args, **kwargs):

        query_extra = request.GET.get("query", None)
        query_next_id = request.GET.get("next", None)
        search_results, next_value = search_youtube(query_extra, query_next_id)

        results = []
        for r in search_results:
            results.append({
                "title": r["title"],
                "link": r["link"],
                "description": r["description"],
                "thumbnail": r["thumbnail"],
            })

        json_results = {
            "results": results,
            "next": next_value,
        }
        return JsonResponse(
            data=json_results
        )

