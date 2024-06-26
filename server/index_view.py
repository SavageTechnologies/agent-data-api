from django.shortcuts import render

from agent.models import Agent
from core.views import BaseView


class IndexView(BaseView):
    requires_login = True

    def get(self, request, *args, **kwargs):
        agent_name = request.GET.get("name", "")
        context = {
            "name": agent_name,
            "search_results": None,
        }
        if agent_name is not None and len(agent_name) > 0:
            agent_query = Agent.objects.filter(name__icontains=agent_name)
            context["search_results"] = agent_query
        return render(request, "index.html", context=context)

