from django.shortcuts import render
from .models import Topic, Flashcards
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render,get_object_or_404

# Create your views here.
def topics(request):
    topics = Topic.objects.all().values()
    template = loader.get_template('topics.html')
    context ={
        'topics':topics,
    }
    return HttpResponse(template.render(context,request))


def flashcards(request, id_topic):
    topic = get_object_or_404(Topic, id_topic=id_topic)
    flashcards_list = Flashcards.objects.filter(id_topic=topic)
    
    context = {
        'topic': topic,
        'flashcards_list': flashcards_list
    }
    
    return render(request, 'topic_detail.html', context)
