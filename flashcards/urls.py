from django.urls import path
from . import views

urlpatterns = [
    path('topics/', views.topics, name='topics'),
    path('flashcards/<int:id_topic>/', views.flashcards, name='flashcards'),
    path('word_detail/<int:id_flashcard>/', views.word_detail, name='word_detail'),
    path('create_topic/',views.create_topic , name ='create_topic'),
    path('create_flashcard/<int:id_topic>/',views.create_flashcard, name = 'create_flashcard'),
    path('success/',views.success_view,name = 'success'),
    path('topics/quiz/', views.quiz_view, name='quiz'), 
]