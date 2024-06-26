from django.shortcuts import render

from core.views import BaseView
from search.serpapi_utils import search_google_local


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

        if query_extra is not None and len(query_extra) > 0:
            locations = []
            if query_city is not None and len(query_city) > 0:
                locations.append(query_city)
            if query_state is not None and len(query_state) > 0:
                locations.append(query_state)
            if query_country is not None and len(query_country) > 0:
                locations.append(query_country)
            location = ", ".join(locations)
            search_results = search_google_local(query_extra, location)
            context["search_results"] = search_results

        return render(request, "serpapi_search.html", context=context)

