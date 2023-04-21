from django.urls import path
from . import views
from .views import SignUpView, HomeView, MediaView, ChatsView
from .consumers import ChatViewWrapper

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("login/", views.sign_in, name="login"),
    path("logout", views.custom_logout, name="logout"),
    path("", HomeView.as_view(), name="home"),
    path("media", MediaView.as_view(), name="media"),
    path("chats/", ChatsView.as_view(), name="chats"),
    path("chats/<int:pk>/", ChatViewWrapper.as_view(), name="chat"),
    path('feeds/<int:feed_id>/like', views.like_feed, name='like_feed'),
    path('feeds/<int:feed_id>/unlike', views.unlike_feed, name='unlike_feed'),
]