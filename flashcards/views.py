from .models import Topic, Flashcards
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render,get_object_or_404,redirect
from .forms import TopicForm, FlashcardsForm

# Create your views here.
def topics(request):
    topics = Topic.objects.all()  # Không sử dụng .values() ở đây
    context = {
        'topics': topics,
    }
    return render(request, 'topics.html', context)



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
        form = TopicForm(request.POST, request.FILES)  # Thêm request.FILES để xử lý file upload
        if form.is_valid():
            form.save()
            return redirect("topics")
    else:
        form = TopicForm()
    return render(request, 'forms.html', {'form': form})

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