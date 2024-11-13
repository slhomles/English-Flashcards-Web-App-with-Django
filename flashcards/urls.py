from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('topics/', views.topics, name='topics'),
    path('flashcards/<slug:slug_topic>/', views.flashcards, name='flashcards'),
    path('word_detail/<slug:slug_flashcard>/', views.word_detail, name='word_detail'),
    path('create_topic/',views.create_topic , name ='create_topic'),
    path('create_flashcard/<slug:slug_topic>/',views.create_flashcard, name = 'create_flashcard'),
    path('success/',views.success_view,name = 'success'),
    path('topics/quiz/', views.quiz_view, name='quiz'), 
    path('hangman/', views.hangman_game, name='hangman'),
]
