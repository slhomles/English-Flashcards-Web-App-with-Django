from django import forms
from .models import Topic, Flashcards

class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['name_topic','image_topic']

class FlashcardsForm(forms.ModelForm):
    class Meta:
        model = Flashcards
        fields = ['front','back']