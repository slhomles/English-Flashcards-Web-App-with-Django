from .models import Topic, Flashcards
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.shortcuts import render,get_object_or_404,redirect
from .forms import TopicForm, FlashcardsForm
import random
from django.core.serializers.json import DjangoJSONEncoder
import json

def topics(request):
    topics = Topic.objects.all().values()
    template = loader.get_template('topics.html')
    context = {
        'topics': topics,
    }
    return HttpResponse(template.render(context, request))


def flashcards(request, id_topic):
    topic = get_object_or_404(Topic, id_topic=id_topic)
    flashcards_list = Flashcards.objects.filter(id_topic=topic)
    context = {
        'topic': topic,
        'flashcards_list': flashcards_list
    }
    
    return render(request, 'topic_detail.html', context)
 
def word_detail(request, id_flashcard):
    word = get_object_or_404(Flashcards, id_flashcard=id_flashcard)
    context = {
        'word': word,
    }
    return render(request, 'word_detail.html', context)

def create_topic(request):
  if request.method == 'POST':
    form = TopicForm(request.POST)
    if form.is_valid():
      form.save()
      return redirect("topics")
  else:
    form = TopicForm()
  return render(request,'forms.html',{'form':form})

def create_flashcard(request,id_topic):
    topic = get_object_or_404(Topic, pk=id_topic)
    form = FlashcardsForm(request.POST)
    if form.is_valid():
         flashcard = form.save(commit = False)
         flashcard.id_topic = topic
         flashcard.save()
         return redirect('flashcards', id_topic=id_topic)
    else:
       form = FlashcardsForm()
    return render(request,'forms.html',{'form': form})


def success_view(request):
  return render(request,'success.html')

def quiz_view(request):
    flashcards = list(Flashcards.objects.all())
    random.shuffle(flashcards)
    questions = []
    
    for i in range(10):
        show = random.choice([True, False])
        if show:
            options = [flashcards[i].back]
            while len(options) < 4:
                random_flashcard = random.choice(flashcards)
                if random_flashcard.back not in options:
                    options.append(random_flashcard.back)
            random.shuffle(options)
            question = {
                "question": flashcards[i].front,
                "options": options,
                "correct_answer": flashcards[i].back
            }
        else:
            options = [flashcards[i].front]
            while len(options) < 4:
                random_flashcard = random.choice(flashcards)
                if random_flashcard.front not in options:
                    options.append(random_flashcard.front)
            random.shuffle(options)
            question = {
                "question": flashcards[i].back,
                "options": options,
                "correct_answer": flashcards[i].front
            }
        questions.append(question)

    return render(request, 'quiz.html', {
       'questions_json': json.dumps(questions, cls=DjangoJSONEncoder)
    })

def hangman_game(request):
    return render(request, 'hangman.html')