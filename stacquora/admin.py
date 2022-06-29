from django.contrib import admin
from .models import Question, Answer
# Register your models here.

admin.site.register(Question)
admin.site.register(Answer)

# @admin.register(Comment)
# class CommentAdmin(admin.ModelAdmin):
#     list_display = ('user','comment', 'object_id', 'content_type')