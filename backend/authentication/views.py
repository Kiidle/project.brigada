from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login
from django.shortcuts import get_object_or_404, redirect, render
from .forms import LoginForm, SignUpForm
from django.urls import reverse_lazy
from django.views import generic

class SignUpView(generic.CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy("login")
    template_name = "signup/signup.html"
def sign_in(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect("/")
        form = LoginForm()
        return render(request, "login/login.html", {"form": form})

    elif request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, f"Erfolgreich angemeldet!")
                return redirect("home")

        messages.error(request, f"Benutzername oder Passwort ist falsch.")
        return render(request, "login/login.html", {"form": form})