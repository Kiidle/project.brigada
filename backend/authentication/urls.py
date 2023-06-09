from django.urls import path
from . import views
from .views import SignUpView, HomeView, MediaView, FeedView, FeedCreateView, FeedUpdateView, ProfileView, SearchView, ChatsView, ForYouView, MyFeedsView, SettingsView
from .consumers import ChatViewWrapper

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("login/", views.sign_in, name="login"),
    path("logout", views.custom_logout, name="logout"),
    path("", HomeView.as_view(), name="home"),
    path("settings", SettingsView.as_view(), name="settings"),
    path("media", MediaView.as_view(), name="media"),
    path("media/foryou", ForYouView.as_view(), name="foryou"),
    path("media/myfeeds", MyFeedsView.as_view(), name="myfeeds"),
    path("media/search", SearchView.as_view(), name="search"),
    path("media/profile-<int:pk>", ProfileView.as_view(), name="profile"),
    path("media/profile-<int:pk>/follow", views.follow_user, name="profile_follow"),
    path("media/profile-<int:pk>/unfollow", views.unfollow_user, name="profile_unfollow"),
    path("media/create", FeedCreateView.as_view(), name="feed_create"),
    path("media/feed-<int:pk>", FeedView.as_view(), name="feed"),
    path("media/feed-<int:pk>/update", FeedUpdateView.as_view(), name="feed_update"),
    path("chats/", ChatsView.as_view(), name="chats"),
    path("chats/<int:pk>/", ChatViewWrapper.as_view(), name="chat"),
    path('feeds/<int:feed_id>/like', views.like_feed, name='like_feed'),
    path('feeds/<int:feed_id>/unlike', views.unlike_feed, name='unlike_feed'),
]