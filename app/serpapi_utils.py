from serpapi import GoogleSearch
import os
from dotenv import load_dotenv

load_dotenv()

SERPAPI_KEY = os.getenv('SERPAPI_KEY')

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
    print(f"Params: {params}")
    print(f"Results: {results}")

    formatted_results = []
    for result in results.get('local_results', []):
        print("Processing result:", result)
        website = result.get("website", "No website available")
        print("Extracted website:", website)
        if website != "No website available" and not website.startswith(('http://', 'https://')):
            website = 'http://' + website
        
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
            "snippet": result.get("snippet"),
            "thumbnail": result.get("thumbnail", {}).get("thumbnails", [{}])[0].get("url")
        })

    return formatted_results[:15]
