from serpapi import GoogleSearch
import os
from dotenv import load_dotenv

from server.settings import SERPAPI_KEY

load_dotenv()


def search_google_local(query, location):
    params = {
        "engine": "google_local",
        "q": query,
        "location": location,
        "api_key": SERPAPI_KEY,
        "output": "json",
        "source": "python"
    }
    search = GoogleSearch(params)
    results = search.get_dict()

    # Enhanced debugging output
    # print(f"Params: {params}")
    # print(f"Results: {results}")

    formatted_results = []
    for result in results.get('local_results', []):
        print("Processing result:", result)
        if "links" in result and "website" in result.get("links"):
            website = result.get("links").get("website")
        else:
            website = None

        formatted_results.append({
            "title": result.get("title"),
            "address": result.get("address", "No address available"),
            "phone": result.get("phone", "No phone number available"),
            "website": website,
            "type": result.get("type", "No type available"),
            "rating": result.get("rating", "No rating available"),
            "reviews": result.get("reviews", "No reviews available"),
        })
    return formatted_results[:15]


def search_youtube(query):
    params = {
        "engine": "youtube",
        "search_query": query,
        "api_key": SERPAPI_KEY
    }
    search = GoogleSearch(params)
    results = search.get_dict()

    formatted_results = []
    for result in results.get('video_results', []):
        formatted_results.append({
            "title": result.get("title"),
            "link": result.get("link"),
            "description": result.get("description"),
            "thumbnail": result.get("thumbnail", {}).get("static")
        })

    return formatted_results[:15]
