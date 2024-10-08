from django.contrib import admin
from .models import Topic, Flashcards

class TopicAdmin(admin.ModelAdmin):
    list_display = ('id_topic','name_topic')

class FlashcardsAdmin(admin.ModelAdmin):
    list_display = ('id_flashcard','front','back')

# Register your models here.
admin.site.register(Topic,TopicAdmin)
admin.site.register(Flashcards,FlashcardsAdmin)