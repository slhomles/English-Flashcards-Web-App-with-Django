from django import forms
from .models import Topic, Flashcards
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['name_topic','image_topic']

    def save(self, user=None, *args, **kwargs):
        topic = super().save(commit=False)
        if user and user.is_authenticated:
            topic.created_by = user
        topic.is_default = False
        topic.save()
        return topic

class FlashcardsForm(forms.ModelForm):
    class Meta:
        model = Flashcards
        fields = ['front','back']

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']