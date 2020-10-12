from django import forms
from django.contrib.auth.models import User
from accounts.models import Profile
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    username = forms.CharField(help_text="")
    class Meta():
        model = User
        fields = ['username','password','email']


class ProfileModelForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'age', 'phone', 'location', 'image', 'cover_photo']