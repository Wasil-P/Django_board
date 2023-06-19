from django import forms

from todolist.models import Post
from user.models import User


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ["title", "tags", "content"]


class EditProfileForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ["username", "email", "profile_picture"]