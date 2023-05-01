from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from datetime import datetime, time
from django.utils.translation import gettext, gettext_lazy as _

class User(AbstractUser):
    pp = models.ImageField(upload_to='static/images/uploads/profile', verbose_name="Profilbild", null=True)
    first_name = models.CharField(max_length=100, verbose_name=_("Vorname"))
    last_name = models.CharField(max_length=100, verbose_name=_("Nachname"))
    username = models.CharField(unique=True, max_length=100, verbose_name=_("Benutzername"))
    majestic_id = models.PositiveIntegerField(null=True, unique=True, verbose_name=_("Majestic ID"))
    email = models.CharField(max_length=100, verbose_name=_("E-Mail Adresse"))
    verified = models.BooleanField(null=False, default=False)

    def get_profile_url(self):
        if self.pp and hasattr(self.pp, 'url'):
            return self.pp.url

class Settings(models.Model):
    class GuiMode(models.TextChoices):
        LIGHTMODE = "Light Mode", "Light Mode"
        DARKMODE = "Dark Mode", "Dark Mode"

    show_fulname = models.BooleanField(null=False, default=True, verbose_name=_("Vollständige Name anzeigen"))
    media = models.BooleanField(null=False, default=False, verbose_name=_("Medien"))
    safemode = models.BooleanField(null=False, default=False, verbose_name=_("Safe Mode"))
    graphic_interface = models.CharField(max_length=50,choices=GuiMode.choices, default=GuiMode.LIGHTMODE, verbose_name=_("Benutzeroberfläche"))
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="settings")

    def __str__(self):
        return f"{self._meta.verbose_name.title()} for {self.user.username}"


class FollowUser(models.Model):
    follower = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    follow = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('follower', 'follow')

    def __str__(self):
        return f"{self.follower} follows {self.follow}"

class FeedManager(models.Manager):
    def liked_by_user(self, feed_id, user_id):
        return self.filter(id=feed_id, likes__user_id=user_id).exists()


class Feed(models.Model):
    description = models.TextField(max_length=200, verbose_name=_("Beschreibung"))
    image = models.ImageField(upload_to='static/images/uploads/feed', verbose_name=_("Bild"))
    published_date = models.DateTimeField(auto_now_add=True, verbose_name=_("Veröffentlicht"))
    visibility = models.BooleanField(null=False, default=True, verbose_name=_("Sichtbar"))
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="feeds")

    def time_since_published(self):
        now = timezone.now()
        diff = now - self.published_date

        if diff.days >= 365:
            count = diff.days // 365
            return _("Vor {count} Jahr{plural}").format(count=count, plural=_('e') if count > 1 else '')
        elif diff.days >= 30:
            count = diff.days // 30
            return _("Vor {count} Monat{plural}").format(count=count, plural=_('e') if count > 1 else '')
        elif diff.days > 0:
            return _("Vor {count} Tag{plural}").format(count=diff.days, plural=_('e') if diff.days > 1 else '')
        elif diff.seconds >= 3600:
            count = diff.seconds // 3600
            return _("Vor {count} Stunde{plural}").format(count=count, plural=_('n') if count > 1 else '')
        elif diff.seconds >= 60:
            count = diff.seconds // 60
            return _("Vor {count} Minute{plural}").format(count=count, plural=_('n') if count > 1 else '')
        else:
            return _("Gerade eben")

    def get_profile_url(self):
        if self.author.pp and hasattr(self.author.pp, 'url'):
            return self.author.pp.url

    def get_image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url

    def __str__(self):
        return self.description

    class Meta:
        ordering = ['-published_date', "-id"]


class FeedLikes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE, related_name='likes')

    def __str__(self):
        return '{} liked {}'.format(self.user.username, self.feed.description)


class Commentary(models.Model):
    content = models.TextField(max_length=200, verbose_name=_("Inhalt"))
    published_date = models.DateField(auto_now_add=True, verbose_name=_("Veröffentlicht"))
    reference = models.ForeignKey(Feed, on_delete=models.CASCADE, related_name="commentaries")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commentaries")

    def __str__(self):
        return self.content

    class Meta:
        ordering = ['-published_date', "-id"]

class Message(models.Model):
    content = models.TextField(max_length=500, verbose_name="Inhalt")
    to = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_messages")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")

    def __str__(self):
        return self.content