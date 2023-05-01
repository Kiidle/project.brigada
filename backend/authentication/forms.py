from django import forms
from django.contrib.auth import get_user_model
from django.forms import ModelForm
from django.core.validators import MaxLengthValidator
from django.utils.translation import gettext_lazy as _
import re
from django.core.validators import MinValueValidator, MaxValueValidator
from .models import Commentary

User = get_user_model()


class SignUpForm(ModelForm):
    first_name = forms.CharField(validators=[MaxLengthValidator(15)], label=_("Vorname"))
    last_name = forms.CharField(validators=[MaxLengthValidator(15)], label=_("Nachname"))
    username = forms.CharField(validators=[MaxLengthValidator(15)], label=_("Benutzername"))
    majestic_id = forms.IntegerField(validators=[MinValueValidator(1000), MaxValueValidator(10000000000)])
    password = forms.CharField(widget=forms.PasswordInput(), label=_("Passwort"))

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "majestic_id",
            "email",
            "password"
        ]
        help_texts = {"username": ""}
        error_messages = {"name": {"required": "Pflichtfeld"}}

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if not username:
            raise forms.ValidationError("Username ist ein Pflichtfeld")
        if " " in username:
            raise forms.ValidationError("Benutzername ist nur diese Format ist erlaubt 'vorname_nachname'. Daten von Majestic!")
        if not re.match("^[a-z0-9_.]+$", username):
            raise forms.ValidationError("Benutzername ist nur diese Format ist erlaubt 'vorname_nachname'. Daten von Majestic!")
        return username.lower()

    def save(self, commit=True):
        user = super().save(commit=commit)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    username = forms.CharField(label=_("Benutzername"))
    password = forms.CharField(widget=forms.PasswordInput, label=_("Passwort"))


class CommentaryForm(forms.ModelForm):
    content = forms.CharField(max_length=200, widget=forms.Textarea(attrs={'rows': 5}), label=_("Inhalt"))

    class Meta:
        model = Commentary
        fields = ["content"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['content'].widget = forms.Textarea(attrs={'rows': 5, 'maxlength': '200'})
