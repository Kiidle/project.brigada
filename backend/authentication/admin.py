from django.contrib import admin
from django.contrib.auth import get_user_model
from authentication.models import Settings, Message, Feed, Commentary, FeedLikes, FollowUser

User = get_user_model()

admin.site.register(User)
admin.site.register(Settings)
admin.site.register(FollowUser)
admin.site.register(Message)
admin.site.register(Feed)
admin.site.register(Commentary)
admin.site.register(FeedLikes)