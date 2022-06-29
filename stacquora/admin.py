from django.contrib import admin
from .models import Question, Answer, QuestionComment, AnswerComment
# Register your models here.

admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(QuestionComment)
admin.site.register(AnswerComment)