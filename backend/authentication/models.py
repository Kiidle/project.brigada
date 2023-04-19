from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    first_name = models.CharField(max_length=100, verbose_name="Vorname")
    last_name = models.CharField(max_length=100, verbose_name="Nachname")
    username = models.CharField(unique=True, max_length=100, verbose_name="Benutzername")
    email = models.CharField(max_length=100, verbose_name="E-Mail Adresse")
    verified = models.BooleanField(null=False, default=False)

class Feed(models.Model):
    description = models.TextField(max_length=200, verbose_name="Beschreibung")
    image = models.ImageField(upload_to='feeds/', verbose_name="Bild")
    published_date = models.DateField(auto_now_add=True, verbose_name="Veröffentlicht")
    visibility = models.BooleanField(null=False, default=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="feeds")

    def __str__(self):
        return self.description

class Commentary(models.Model):
    content = models.TextField(max_length=200, verbose_name="Inhalt")
    published_date = models.DateField(auto_now_add=True, verbose_name="Veröffentlicht")
    reference = models.ForeignKey(Feed, on_delete=models.CASCADE, related_name="commentaries")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commentaries")

    def __str__(self):
        return self.content

class message(models.Model):
    content = models.TextField(max_length=500, verbose_name="Inhalt")
    to = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_messages")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")

    def __str__(self):
        return self.content