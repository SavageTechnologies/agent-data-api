from django import forms
from django.http import HttpRequest
from django.shortcuts import redirect, render

from core.views import BaseView
from user.models import User


# Create your views here.


class LoginView(BaseView):
    class LoginForm(forms.Form):
        email = forms.EmailField(required=True)
        password = forms.CharField(widget=forms.PasswordInput, required=True)

    def _handle_view(self, request: HttpRequest, is_get: bool):
        if self.user is not None:
            redirect_fragment = request.GET.get("r", "/")
            return redirect(redirect_fragment, permanent=False)

        if is_get:
            form = LoginView.LoginForm()
        else:
            form = LoginView.LoginForm(request.POST)
            print(request.POST)
            if form.is_valid():
                user: User = User.objects.filter(username=form.cleaned_data['email']).first()
                if user is not None:
                    password = form.cleaned_data['password']
                    if user.check_password(password):
                        self.login(user)
                        redirect_fragment = request.GET.get("r", "/")
                        return redirect(redirect_fragment, permanent=False)

        context = {
            "form": form,
            "hide_header": True,
        }
        return render(request, template_name="login.html", context=context)
    def get(self, request):
        return self._handle_view(request, True)

    def post(self, request):
        return self._handle_view(request, False)


class LogoutView(BaseView):
    def get(self, request):
        self.logout()
        return redirect("/user/login/", permanent=False)



