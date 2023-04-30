from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.db.models import Prefetch
from django.shortcuts import get_object_or_404, redirect, render, reverse
from .forms import LoginForm, SignUpForm, CommentaryForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import Group
from .models import Settings, Feed, FeedLikes, Commentary
from django.http import HttpResponseRedirect, JsonResponse
from urllib.parse import urlencode
from django.db.models.signals import post_save
from django.dispatch import receiver

User = get_user_model()


class SignUpView(generic.CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy("login")
    template_name = "signup/signup.html"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        group, created = Group.objects.get_or_create(name='citizen')
        if created:
            print("Group 'citizen' created successfully.")
        else:
            print("Group 'citizen' already exists.")
        group, created = Group.objects.get_or_create(name='hoodlum')
        if created:
            print("Group 'hoodlum' created successfully.")
        else:
            print("Group 'hoodlum' already exists.")
        group, created = Group.objects.get_or_create(name='lica')
        if created:
            print("Group 'lica' created successfully.")
        else:
            print("Group 'lica' already exists.")
        group, created = Group.objects.get_or_create(name='byk')
        if created:
            print("Group 'byk' created successfully.")
        else:
            print("Group 'byk' already exists.")
        group, created = Group.objects.get_or_create(name='wolk')
        if created:
            print("Group 'wolk' created successfully.")
        else:
            print("Group 'wolk' already exists.")
        group, created = Group.objects.get_or_create(name='bojewik')
        if created:
            print("Group 'bojewik' created successfully.")
        else:
            print("Group 'bojewik' already exists.")
        group, created = Group.objects.get_or_create(name='soldat')
        if created:
            print("Group 'soldat' created successfully.")
        else:
            print("Group 'soldat' already exists.")
        group, created = Group.objects.get_or_create(name='sovietnik')
        if created:
            print("Group 'sovietnik' created successfully.")
        else:
            print("Group 'sovietnik' already exists.")
        group, created = Group.objects.get_or_create(name='brigadier')
        if created:
            print("Group 'brigadier' created successfully.")
        else:
            print("Group 'brigadier' already exists.")
        group, created = Group.objects.get_or_create(name='medved')
        if created:
            print("Group 'medved' created successfully.")
        else:
            print("Group 'medved' already exists.")
        group, created = Group.objects.get_or_create(name='lew')
        if created:
            print("Group 'lew' created successfully.")
        else:
            print("Group 'lew' already exists.")

    @receiver(post_save, sender=User)
    def create_user_privacy(sender, instance, created, **kwargs):
        if created:
            Settings.objects.create(user=instance)

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


class MediaView(generic.ListView):
    model = Feed
    fields = ["description", "image", "published_date", "visibility", "author"]
    template_name = "media/media.html"
    login_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["feeds"] = super().get_queryset().order_by("-published_date", "-id")
        feed_likes = FeedLikes.objects.all()
        unlike_flag = []
        for feed in context["feeds"]:
            liked = feed_likes.filter(feed_id=feed.id, user_id=self.request.user.id).exists()
            if not liked:
                unlike_flag.append(feed.id)
        context["unlike_flag"] = unlike_flag

        return context

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(self.login_url)
        else:
            return super().get(request, *args, **kwargs)


def like_feed(request, feed_id):
    feed = get_object_or_404(Feed, id=feed_id)
    if not FeedLikes.objects.filter(user=request.user, feed=feed).exists():
        FeedLikes.objects.create(user=request.user, feed=feed)
        likes_count = FeedLikes.objects.filter(feed_id=feed_id).count()
    return HttpResponseRedirect(reverse('feed', args=[feed_id]))


def unlike_feed(request, feed_id):
    feed = get_object_or_404(Feed, id=feed_id)
    try:
        like = FeedLikes.objects.get(feed=feed, user=request.user)
        like.delete()
        likes_count = FeedLikes.objects.filter(feed_id=feed_id).count()
        return HttpResponseRedirect(reverse('feed', args=[feed_id]))
    except FeedLikes.DoesNotExist:
        return HttpResponseRedirect(reverse('feed', args=[feed_id]))


class FeedView(generic.DetailView):
    model = Feed
    fields = ["description", "image", "published_date", "visibility", "author", "commentaries"]
    template_name = "feeds/feed.html"
    login_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["feeds"] = super().get_queryset().order_by("-id", "image")

        feed_likes = FeedLikes.objects.all()
        unlike_flag = []
        for feed in context["feeds"]:
            liked = feed_likes.filter(feed_id=feed.id, user_id=self.request.user.id).exists()
            if not liked:
                unlike_flag.append(feed.id)
        context["unlike_flag"] = unlike_flag

        context['commentaries'] = self.object.commentaries.order_by('-published_date', "-id")
        context['commentary_form'] = CommentaryForm()

        return context

    def get_success_url(self):
        return reverse_lazy('feed', kwargs={'pk': self.kwargs['pk']})

    def post(self, request, *args, **kwargs):
        form = CommentaryForm(request.POST)
        if form.is_valid():
            commentary = form.save(commit=False)
            commentary.author = request.user
            commentary.reference = self.get_object()
            commentary.save()
        return redirect('feed', pk=self.get_object().pk)

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(self.login_url)
        else:
            return super().get(request, *args, **kwargs)


class FeedCreateView(generic.CreateView):
    model = Feed
    fields = ["description", "image", "visibility"]
    template_name = "feeds/form.html"

    def get_success_url(self):
        return reverse_lazy('media')

    def form_valid(self, form):
        form.instance.author = self.request.user

        return super().form_valid(form)


class FeedUpdateView(generic.UpdateView):
    model = Feed
    fields = ["description", "image", "visibility"]
    template_name = "feeds/form.html"

    def get_success_url(self):
        return reverse_lazy("feed", args=[self.object.pk])

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_initial(self):
        initial = super().get_initial()
        initial['image'] = self.object.image
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ProfileView(generic.DetailView):
    model = User
    fields = ["first_name", "last_name", "username" "verified"]
    template_name = "media/profile.html"
    login_url = reverse_lazy('login')

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(self.login_url)
        else:
            return super().get(request, *args, **kwargs)


class SearchView(generic.ListView):
    model = User
    fields = ["first_name", "last_name", "username" "verified"]
    template_name = 'media/search.html'

    login_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["users"] = super().get_queryset().order_by("first_name", "last_name", "username")

        return context

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

        context["users"] = super().get_queryset().order_by("first_name", "last_name")

        return context

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(self.login_url)
        else:
            return super().get(request, *args, **kwargs)
