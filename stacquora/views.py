from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from .models import Answer, Question
from .forms import LoginForm,UserRegistrationForm,AskQuestionForm,AnswerQuestion
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from taggit.models import Tag
# Create your views here.

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authenticated Successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form':form})


def homepage(request, tag_slug=None):
    sort = request.GET.get('order','-created')
    questions = Question.objects.all().order_by(sort)
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        questions = questions.filter(tags__in=[tag])

    return render(request, 'stacquora/homepage.html', {'section': 'homepage', 'questions':questions,'tag':tag})


def register(request):
    if request.method=='POST':
        user_form=UserRegistrationForm(request.POST)

        if user_form.is_valid():
            new_user=user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            return render(request, 'stacquora/registered.html', {'new_user':new_user})
    else:
        user_form=UserRegistrationForm()
    return render(request, 'stacquora/register.html', {'user_form':user_form})

@login_required
def askquestion(request):
    form = AskQuestionForm()

    if request.method=="POST":
        form = AskQuestionForm(request.POST)

        if form.is_valid():
            question=form.save(commit=False)
            question.author=request.user
            question.save()

    return render(request, 'stacquora/askquestion.html', {'form':form})

def questionpage(request, id):
    question = Question.objects.get(id=id)
    answerform = AnswerQuestion()

    if request.method=='POST':
        answerform = AnswerQuestion(request.POST)

        if answerform.is_valid():
            answer=answerform.save(commit=False)
            answer.user=request.user
            answer.question=Question(id=id)
            answer.save()


    return render(request, 'stacquora/question_detail.html',{'question':question, 'answerform':answerform })

