from django import forms
from .models import Topic, Flashcards
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['name_topic','image_topic']

class FlashcardsForm(forms.ModelForm):
    class Meta:
        model = Flashcards
        fields = ['front','back']

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']