from django import forms

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm

class EditProfile(UserChangeForm):

    password = None

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')
