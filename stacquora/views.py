from django.shortcuts import redirect, render
from stacquora.filters import QuestionFilter
from .models import Answer, AnswerComment, Question, QuestionComment
from .forms import UserRegistrationForm,AskQuestionForm,AnswerQuestion, QuestionCommentForm, AnswerCommentForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from voting.models import Vote
from django.views.generic.list import ListView
from django.views.generic import FormView
from django.views.generic.edit import CreateView,UpdateView
from django_filters.views import FilterView
from .filters import QuestionFilter
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.

class HomePageFilterMixin(FilterView, ListView):
    model = Question
    paginate_by = 3
    filterset_class = QuestionFilter
    ordering = ['created']

class QuestionList(HomePageFilterMixin):
    template_name = "stacquora/homepage.html"


class RegisterView(CreateView):
    form_class = UserRegistrationForm
    template_name = 'stacquora/register.html'

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()
        return render(self.request, 'stacquora/registered.html')
    
class AskQuestionView(LoginRequiredMixin, CreateView):
    form_class = AskQuestionForm
    template_name = 'stacquora/askquestion.html'

    def form_valid(self, form):
        question=form.save(commit=False)
        question.author=self.request.user
        question.save()
        return redirect('homepage')

# class AnswerAQuestion(FormView):
#     form_class = AnswerQuestion
#     model = Question
#     template_name = 'stacquora/question_detail.html'

#     def form_valid(self, form):
#         answer=form.save(commit=False)
#         answer.user=self.request.user
#         answer.question=Question(id=self.kwargs['id'])
#         answer.save()
#         return redirect(reverse('question', args=['id']))

def questionpage(request, id):
    question = Question.objects.get(id=id)
    answerform = AnswerQuestion()

    answerform = AnswerQuestion(request.POST or None)

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

# def updown_helper(request, model_object, vote, id, related_name=None):
#     user = request.user
#     model = model_object.objects.get(id=id)
#     related_model = getattr(model, related_name) if related_name else model
    
#     if vote==1:
#         Vote.objects.record_vote(model, user, +1)
#     elif vote==2:
#         Vote.objects.record_vote(model, user, 0)

#     if model_object==Question:
#         return redirect('homepage')
#     else:
#         q_id = related_model.question_id
#         return redirect(reverse('question', args=[q_id]))

    
# def questionupdown(request, id, vote):
#     return updown_helper(request, Question, vote, id)

# def answerupdown(request, id, vote):
#     return updown_helper(request, Answer, vote, id)

# def questioncommentupdown(request, id, vote):
#     return updown_helper(request, QuestionComment, vote, id)

# def answercommentupdown(request, id, vote):
#     return updown_helper(request, AnswerComment, vote, id, "answer")


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