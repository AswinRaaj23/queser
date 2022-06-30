from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager

from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType

# Create your models here.
class Question(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField(null=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    tags = TaggableManager()
    
    def __str__(self):
        return self.title

class Answer(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, null=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=False, related_name='answers')
    answer = models.TextField(null=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.answer

class QuestionComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null= False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=False, related_name='questioncomment')
    comment = models.CharField(max_length=300)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment

class AnswerComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null= False)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, null=False, related_name='answercomment')
    comment = models.CharField(max_length=300)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment