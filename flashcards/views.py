from .models import Topic, Flashcards
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.shortcuts import render,get_object_or_404,redirect
from .forms import TopicForm, FlashcardsForm
import random
from django.core.serializers.json import DjangoJSONEncoder
import json
from django.urls import reverse
from .forms import RegistrationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render

def topics(request):
    if request.user.is_authenticated:
        # Lấy topic mặc định và topic do người dùng đăng nhập tạo ra
        topics = Topic.objects.filter(is_default=True) | Topic.objects.filter(created_by=request.user)
    else:
        # Chỉ hiển thị topic mặc định cho người dùng chưa đăng nhập
        topics = Topic.objects.filter(is_default=True)

    return render(request, 'topics.html', {'topics': topics})



def flashcards(request, slug_topic):
    topic = get_object_or_404(Topic, slug_topic=slug_topic)
    flashcards_list = Flashcards.objects.filter(id_topic__slug_topic=topic)
    context = {
        'topic': topic,
        'flashcards_list': flashcards_list
    }
    
    return render(request, 'topic_detail.html', context)
 
def word_detail(request, slug_flashcard):
    word = get_object_or_404(Flashcards, slug_flashcard=slug_flashcard)
    context = {
        'word': word,
    }
    return render(request, 'word_detail.html', context)

def create_topic(request):
    if request.method == 'POST':
        form = TopicForm(request.POST, request.FILES)  # Thêm request.FILES để xử lý file upload
        if form.is_valid():
            form.save(user=request.user)
            return redirect("topics")
    else:
        form = TopicForm()
    return render(request, 'forms.html', {'form': form})

def create_flashcard(request,slug_topic):
    #topic = get_object_or_404(Topic, pk=slug_topic)
    topic = get_object_or_404(Topic, slug_topic=slug_topic)
    form = FlashcardsForm(request.POST)
    if form.is_valid():
         flashcard = form.save(commit = False)
         flashcard.id_topic = topic
         flashcard.save()
         return redirect('flashcards', slug_topic=slug_topic)
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
    flashcards = Flashcards.objects.all()
    if flashcards:
        random_flashcard = random.choice(flashcards)
        hangman_word = random_flashcard.front
    else:
        hangman_word = ""
    context = {
        "hangman_word": hangman_word.upper(),
    }
    return render(request, 'hangman.html', context)

def delete_topic(request, id_topic):
    topic = get_object_or_404(Topic, id_topic=id_topic)
    topic.delete()
    
    return redirect('topics')

def delete_flashcard(request, id_flashcard):
    flashcard = get_object_or_404(Flashcards, id_flashcard=id_flashcard)
    flashcard.delete()

    return redirect(request.META.get('HTTP_REFERER', '/'))

def custom_topic(request, id_topic):
    topic = get_object_or_404(Topic, id_topic=id_topic)  
    if request.method == 'POST':
        form = TopicForm(request.POST, request.FILES, instance=topic)  
        if form.is_valid():
            form.save()  
            return redirect('topics')  
    else:
        form = TopicForm(instance=topic)  
    return render(request, 'forms.html', {'form': form})

def custom_flashcard(request, id_flashcard):
    flashcard = get_object_or_404(Flashcards, id_flashcard=id_flashcard)
    topic = flashcard.id_topic 

    if request.method == 'POST':
        form = FlashcardsForm(request.POST, instance=flashcard)
        if form.is_valid():
            flashcard = form.save(commit=False)
            flashcard.id_topic = topic  
            flashcard.save()
            return redirect(reverse('flashcards', kwargs={'slug_topic': topic.slug_topic}))
    else:
        form = FlashcardsForm(instance=flashcard)

    return render(request, 'forms.html', {'form': form})
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()  # Lưu người dùng vào database
            messages.success(request, 'Tài khoản của bạn đã được tạo thành công!')
            return redirect('topics')  # Điều hướng đến trang đăng nhập hoặc trang khác
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Đăng nhập thành công!')
            return redirect('topics')  # Thay 'home' bằng tên view hoặc URL bạn muốn chuyển đến sau đăng nhập
        else:
            messages.error(request, 'Tên đăng nhập hoặc mật khẩu không đúng.')
    return render(request, 'login.html')  # Trang HTML hiển thị form đăng nhập

def logout_view(request):
    logout(request)
    messages.info(request, 'Bạn đã đăng xuất.')
    return redirect('topics')

