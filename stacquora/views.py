from django.http import HttpResponse
from django.shortcuts import render
from .models import Question
from .forms import LoginForm,UserRegistrationForm,AskQuestionForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
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


def homepage(request):
    questions = Question.objects.all().order_by('-created')

    return render(request, 'stacquora/homepage.html', {'section': 'homepage', 'questions':questions})


def questionpage(request):
    return None

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