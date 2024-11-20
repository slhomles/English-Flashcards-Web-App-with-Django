from django.contrib import admin
from .models import Topic, Flashcards, Study

class TopicAdmin(admin.ModelAdmin):
    list_display = ('id_topic','name_topic')

class FlashcardsAdmin(admin.ModelAdmin):
    list_display = ('id_flashcard','front','back')


class StudyAdmin(admin.ModelAdmin):
    list_display = ('id_study', 'start_time', 'end_time', 'id_user')

# Register your models here.
admin.site.register(Topic,TopicAdmin)
admin.site.register(Flashcards,FlashcardsAdmin)
admin.site.register(Study, StudyAdmin)