from django.shortcuts import get_object_or_404, redirect, render
from .models import Answer, Question, QuestionComment
from .forms import LoginForm,UserRegistrationForm,AskQuestionForm,AnswerQuestion, QuestionComment
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from taggit.models import Tag
# Create your views here.

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

@login_required
def edit(request, id):
    question = Question.objects.get(id=id)
    if request.method=='POST':
        edit_form = AskQuestionForm(instance=question, data=request.POST)
        if edit_form.is_valid():
            edit_form.save()
            return redirect('homepage')
    else:
        edit_form = AskQuestionForm(instance=question)
    return render(request,'stacquora/edit.html', {'edit_form':edit_form})

@login_required
def edit_answer(request, id):
    answer = Answer.objects.get(id=id)
    if request.method=='POST':
        edit_answer_form = AnswerQuestion(instance=answer, data=request.POST)
        if edit_answer_form.is_valid():
            edit_answer_form.save()
            return redirect('homepage')
    else:
        edit_answer_form = AnswerQuestion(instance=answer)
    return render(request, 'stacquora/edit_answer.html', {'edit_answer_form':edit_answer_form})

@login_required
def delete(request, id):
    question = Question.objects.get(id=id)
    question.delete()
    return redirect('homepage')

@login_required
def delete_answer(request, id):
    answer = Answer.objects.get(id=id)
    answer.delete()
    return redirect('homepage')


def questioncomment(request, id):
    commentform = QuestionComment
    question = Question.objects.get(id=id)

    if request.method=='POST':
        commentform = QuestionComment(request.POST)

        if commentform.is_valid():
            comment=commentform.save(commit=False)
            comment.user=request.user
            comment.question=Question(id=id)
            comment.save()
            return redirect('homepage')

    return render(request, 'stacquora/question_comment.html', {'commentform':commentform, 'question':question})