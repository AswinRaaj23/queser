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
    path('', views.homepage, name='homepage'),
    path('tag/<slug:tag_slug>/', views.homepage, name='question_list_by_tag'),
]
