from django import forms
from .models import Article
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content', 'is_published']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 10})
        }


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Email")

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user