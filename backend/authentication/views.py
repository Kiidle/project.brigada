from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.shortcuts import get_object_or_404, redirect, render, reverse
from .forms import LoginForm, SignUpForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import Group
from authentication.models import Message
from django.views.decorators.csrf import csrf_exempt
from .models import Message
from channels.generic.websocket import AsyncWebsocketConsumer
import json

User = get_user_model()


class SignUpView(generic.CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy("login")
    template_name = "signup/signup.html"

    group, created = Group.objects.get_or_create(name='citizen')
    if created:
        print("Group 'citizen' created successfully.")
    else:
        print("Group 'citizen' already exists.")

    def form_valid(self, form):
        response = super().form_valid(form)
        group = Group.objects.get(name="citizen")
        self.object.groups.add(group)
        return response


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


@login_required
def custom_logout(request):
    logout(request)
    return redirect("login")


class HomeView(generic.ListView):
    model = User
    template_name = "home/home.html"
    login_url = reverse_lazy('login')

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(self.login_url)
        else:
            return super().get(request, *args, **kwargs)


class ChatsView(generic.ListView):
    model = User
    fields = ["first_name", "last_name"]
    template_name = "chats/chats.html"
    login_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["users"] = super().get_queryset().order_by('first_name', 'last_name')

        print(context)

        return context

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(self.login_url)
        else:
            return super().get(request, *args, **kwargs)



