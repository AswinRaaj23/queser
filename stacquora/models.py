from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
from model_utils.models import TimeStampedModel

from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType

# Create your models here.
class Question(TimeStampedModel):
    title = models.CharField(max_length=250)
    description = models.TextField(null=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    tags = TaggableManager()

    def __str__(self):
        return self.title

class Answer(TimeStampedModel):
    user = models.ForeignKey(User, on_delete = models.CASCADE, null=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=False, related_name='answers')
    answer = models.TextField(null=False)
    
    def __str__(self):
        return self.answer

class QuestionComment(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null= False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=False, related_name='questioncomment')
    comment = models.CharField(max_length=300)
    
    def __str__(self):
        return self.comment

class AnswerComment(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null= False)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, null=False, related_name='answercomment')
    comment = models.CharField(max_length=300)
    
    def __str__(self):
        return self.comment