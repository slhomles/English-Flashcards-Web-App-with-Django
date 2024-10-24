from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('topics/', views.topics, name='topics'),
    path('flashcards/<int:id_topic>/', views.flashcards, name='flashcards'),
    path('word_detail/<int:id_flashcard>/', views.word_detail, name='word_detail'),
    path('create_topic/',views.create_topic , name ='create_topic'),
    path('create_flashcard/<int:id_topic>/',views.create_flashcard, name = 'create_flashcard'),
    path('success/',views.success_view,name = 'success'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)