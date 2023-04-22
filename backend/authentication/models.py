from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    pp = models.ImageField(upload_to='static/images/uploads/profile', verbose_name="Profilbild", null=True)
    first_name = models.CharField(max_length=100, verbose_name="Vorname")
    last_name = models.CharField(max_length=100, verbose_name="Nachname")
    username = models.CharField(unique=True, max_length=100, verbose_name="Benutzername")
    email = models.CharField(max_length=100, verbose_name="E-Mail Adresse")
    verified = models.BooleanField(null=False, default=False)

    def get_profile_url(self):
        if self.pp and hasattr(self.pp, 'url'):
            return self.pp.url

class FeedManager(models.Manager):
    def liked_by_user(self, feed_id, user_id):
        return self.filter(id=feed_id, likes__user_id=user_id).exists()

class Feed(models.Model):
    description = models.TextField(max_length=200, verbose_name="Beschreibung")
    image = models.ImageField(upload_to='static/images/uploads/feed', verbose_name="Bild")
    published_date = models.DateField(auto_now_add=True, verbose_name="Veröffentlicht")
    visibility = models.BooleanField(null=False, default=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="feeds")

    def get_profile_url(self):
        if self.author.pp and hasattr(self.author.pp, 'url'):
            return self.author.pp.url

    def get_image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url

    def __str__(self):
        return self.description

class FeedLikes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE, related_name='likes')
    def __str__(self):
        return '{} liked {}'.format(self.user.username, self.feed.description)

class Commentary(models.Model):
    content = models.TextField(max_length=200, verbose_name="Inhalt")
    published_date = models.DateField(auto_now_add=True, verbose_name="Veröffentlicht")
    reference = models.ForeignKey(Feed, on_delete=models.CASCADE, related_name="commentaries")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commentaries")

    def __str__(self):
        return self.content

class Message(models.Model):
    content = models.TextField(max_length=500, verbose_name="Inhalt")
    to = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_messages")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")

    def __str__(self):
        return self.content

class Stone(models.Model):
    pass

class Wood(models.Model):
    pass