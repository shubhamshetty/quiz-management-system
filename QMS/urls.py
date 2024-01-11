"""QMS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home,name='home'),
    path('admin',views.admin,name='admin'),
    path('login',views.checkuser,name='login'),
    path('register', views.register_user, name="register"),
    #path('student',views.student,name='student'),
    path('create_quiz',views.create_quiz,name='create_quiz'),
    path('View_quizzes',views.view_all_quizzes,name='view_quizzes'),
    path('view_quiz_qa/<int:id>',views.view_quiz,name='view_quiz_qa'),
    path('modify_quiz',views.modify_quizzes,name = 'modify'),
    path('modify/<int:id>',views.quiz_to_be_modified,name='modify_quiz'),
    path('update/<int:id>',views.update_quiz,name='update'),
    path('delete',views.show_quizzes,name='delete'),
    path('delete/<int:id>',views.delete_quiz,name='delete_quiz'),
    #path('student_login', views.user_login_page, name="Login form"),
    #path('register_student/', views.register_user, name="Register User"),
    #path('quiz_dashboard/<str:student_id>', views.quiz_dashboard, name="quiz_dashboard"),
    path('quiz_dashboard/<str:student_id>/<int:category_id>', views.quiz_dashboard, name="quiz_dashboard"),
    path('submit_quiz/<str:unique_id>/<int:quiz_id>/<int:category_id>', views.submit_quiz, name="submit_quiz"),
    #path('take_quiz/<int:category_id>/<int:quiz_id>/<str:unique_id>/submit_quiz/<str:unique_id>/<int:quiz_id>/<int:category_id>',views.submit_quiz,name='submit_quiz'),
    path('take_quiz/<int:category_id>/<int:quiz_id>/<str:unique_id>', views.take_quiz, name="take_quiz"),
    path('view_stats/<int:quiz_id>/<str:unique_id>', views.view_stats, name="view_stats"),
    path('change_password',views.forgot_password,name ='forgot_password'),
    path('quiz_results/<int:id>',views.quiz_result,name='quiz_result'),
    path('delete_question/<int:id>',views.delete_question,name='delete_question'),
    path('add_question/<int:id>',views.add_question,name='add_question')
]
