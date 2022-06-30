from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('askquestion/', views.askquestion, name='askquestion'),
    path('question/<int:id>/', views.questionpage, name='question'),
    path('edit/<int:id>/', views.edit, name='edit'),
    path('editanswer/<int:id>/', views.edit_answer, name='edit_answer'),
    path('delete/<int:id>/', views.delete, name='delete'),
    path('deleteanswer/<int:id>/', views.delete_answer, name='delete_answer'),
    path('questioncomment/<int:id>/', views.questioncomment, name='question_comment'),
    path('answercomment/<int:id>/', views.answercomment, name='answer_comment'),
    path('editquestion-comment/<int:id>/', views.edit_questioncomment, name='edit_comment_for_question'),
    path('editanswer-comment/<int:id>/', views.edit_answercomment, name='edit_comment_for_answer'),
    path('delete-questioncomment/<int:id>/', views.delete_questioncomment, name='delete_comment_for_question'),
    path('delete-answercomment/<int:id>/', views.delete_answercomment, name='delete_comment_for_answer'),
    path('', views.homepage, name='homepage'),
    path('questionupdownvote/<int:id>/<int:vote>', views.questionupdown, name='questionupdown'),
    path('answerupdownvote/<int:id>/<int:vote>', views.answerupdown, name='answerupdown'),
    path('tag/<slug:tag_slug>/', views.homepage, name='question_list_by_tag'),
]
