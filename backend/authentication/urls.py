from django.urls import path
from . import views
from .views import SignUpView, HomeView, ChatsView

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("login/", views.sign_in, name="login"),
    path("logout", views.custom_logout, name="logout"),
    path("", HomeView.as_view(), name="home"),
    path("chats/", ChatsView.as_view(), name="chats")
]