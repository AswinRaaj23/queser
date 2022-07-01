from django.shortcuts import get_object_or_404, redirect, render
from .models import Answer, AnswerComment, Question, QuestionComment
from .forms import LoginForm,UserRegistrationForm,AskQuestionForm,AnswerQuestion, QuestionCommentForm, AnswerCommentForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from taggit.models import Tag
from django.urls import reverse
from voting.models import Vote
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.

def homepage(request, tag_slug=None):
    sort = request.GET.get('order','-created')
    questions = Question.objects.all().order_by(sort)
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        questions = questions.filter(tags__in=[tag])

    paginator = Paginator(questions, 3)
    page = request.GET.get('page')

    try:
        questions = paginator.page(page)
    except PageNotAnInteger:
        questions = paginator.page(1)
    except EmptyPage:
        questions = paginator.page(paginator.num_pages)

    return render(request, 'stacquora/homepage.html', {'section': 'homepage', 'questions':questions,'tag':tag, 'page':page})


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
            return redirect('homepage')

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
            return redirect(reverse('question', args=[id]))


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
    q_id = answer.question.id
    if request.method=='POST':
        edit_answer_form = AnswerQuestion(instance=answer, data=request.POST)
        if edit_answer_form.is_valid():
            edit_answer_form.save()
            return redirect(reverse('question', args=[q_id]))
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
    q_id = answer.question.id
    answer.delete()
    return redirect(reverse('question', args=[q_id]))

@login_required
def questioncomment(request, id):
    commentform = QuestionCommentForm
    question = Question.objects.get(id=id)

    if request.method=='POST':
        commentform = QuestionCommentForm(request.POST)

        if commentform.is_valid():
            comment=commentform.save(commit=False)
            comment.user=request.user
            comment.question=Question(id=id)
            comment.save()
            return redirect(reverse('question', args=[id]))

    return render(request, 'stacquora/question_comment.html', {'commentform':commentform, 'question':question})

@login_required
def answercomment(request, id):
    anscommentform = AnswerCommentForm
    answer = Answer.objects.get(id=id)
    q_id = answer.question.id

    if request.method=='POST':
        anscommentform = AnswerCommentForm(request.POST)

        if anscommentform.is_valid():
            comment=anscommentform.save(commit=False)
            comment.user=request.user
            comment.answer=Answer(id=id)
            comment.save()
            return redirect(reverse('question', args=[q_id]))
    
    return render(request, 'stacquora/answer_comment.html', {'anscommentform':anscommentform, 'answer':answer})


@login_required
def edit_questioncomment(request, id):
    comment = QuestionComment.objects.get(id=id)
    q_id = comment.question.id

    if request.method=='POST':
        edit_comment_form = QuestionCommentForm(instance=comment, data=request.POST)
        if edit_comment_form.is_valid():
            edit_comment_form.save()
            return redirect(reverse('question', args=[q_id]))
    else:
        edit_comment_form = QuestionCommentForm(instance=comment)
    return render(request, 'stacquora/edit_questioncomment.html', {'edit_comment_form':edit_comment_form})

@login_required
def edit_answercomment(request, id):
    comment = AnswerComment.objects.get(id=id)
    q_id = comment.answer.question.id

    if request.method=='POST':
        edit_answercomment_form = AnswerCommentForm(instance=comment, data=request.POST)
        if edit_answercomment_form.is_valid():
            edit_answercomment_form.save()
            return redirect(reverse('question', args=[q_id]))
    else:
        edit_answercomment_form = AnswerCommentForm(instance=comment)

    return render(request, 'stacquora/edit_answercomment.html', {'edit_answercomment_form':edit_answercomment_form})

@login_required
def delete_questioncomment(request, id):
    comment = QuestionComment.objects.get(id=id)
    q_id = comment.question.id

    comment.delete()
    return redirect(reverse('question', args=[q_id]))

@login_required
def delete_answercomment(request, id):
    comment = AnswerComment.objects.get(id=id)
    q_id = comment.answer.question.id

    comment.delete()
    return redirect(reverse('question', args=[q_id]))

def questionupdown(request, id, vote):
    user = request.user
    question = Question.objects.get(id=id)

    if vote==1:
        Vote.objects.record_vote(question, user, +1)
    elif vote==2:
        Vote.objects.record_vote(question, user, 0)
    return redirect('homepage')

def answerupdown(request, id, vote):
    user = request.user
    answer = Answer.objects.get(id=id)
    q_id = answer.question.id

    if vote==1:
        Vote.objects.record_vote(answer, user, +1)
    elif vote==2:
        Vote.objects.record_vote(answer, user, 0)
    return redirect(reverse('question', args=[q_id]))

def questioncommentupdown(request, id, vote):
    user = request.user
    comment = QuestionComment.objects.get(id=id)
    q_id = comment.question.id

    if vote==1:
        Vote.objects.record_vote(comment, user, +1)
    elif vote==2:
        Vote.objects.record_vote(comment, user, 0)
    return redirect(reverse('question', args=[q_id]))


def answercommentupdown(request, id, vote):
    user = request.user
    comment = AnswerComment.objects.get(id=id)
    q_id = comment.answer.question.id
    
    if vote==1:
        Vote.objects.record_vote(comment, user, +1)
    elif vote==2:
        Vote.objects.record_vote(comment, user, 0)
    return redirect(reverse('question', args=[q_id]))