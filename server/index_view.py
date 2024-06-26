from django.shortcuts import render

from core.views import BaseView


class IndexView(BaseView):
    requires_login = True

    def get(self, request, *args, **kwargs):
        return render(request, "index.html")

