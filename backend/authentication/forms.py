from django import forms
from django.contrib.auth import get_user_model
from django.forms import ModelForm
from django.core.validators import MaxLengthValidator
from django.utils.translation import gettext_lazy as _

User = get_user_model()

class SignUpForm(ModelForm):
    first_name= forms.CharField(validators=[MaxLengthValidator(15)], label=_("Vorname"))
    last_name= forms.CharField(validators=[MaxLengthValidator(15)], label=_("Nachname"))
    password = forms.CharField(widget=forms.PasswordInput(), label=_("Passwort"))

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
            "password"
        ]
        help_texts = {"username": ""}
        error_messages = {"name": {"required": "Pflichtfeld"}}

    def save(self, commit=True):
        user = super().save(commit=commit)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

class LoginForm(forms.Form):
    username = forms.CharField(label=_("Benutzername"))
    password = forms.CharField(widget=forms.PasswordInput, label=_("Passwort"))