from django import forms
from django.contrib.auth.models import User
from .models import Journal, Comment
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.utils.translation import gettext_lazy as _
from core.models import Category

class JournalModelForm(forms.ModelForm):
    class Meta:
        model = Journal
        fields = ['Your_Post_Title', 'image', 'Link', 'Content']


class CommentForm(forms.Form):
    content_type = forms.CharField(widget=forms.HiddenInput,help_text="")
    object_id = forms.IntegerField(widget=forms.HiddenInput, help_text="")
    #parent_id = forms.IntegerField(widget=forms.HiddenInput, required=False)
    content = forms.CharField(label='', help_text="")


