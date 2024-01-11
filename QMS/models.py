from django.db import models
from django.utils import timezone

class Login(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    is_student = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    unique_id = models.CharField(max_length=100, blank=True)

class Student(models.Model):
    student_name = models.CharField(max_length=100)
    quiz_id = models.IntegerField()
    score = models.IntegerField()
    unique_id = models.CharField(max_length=100)
    no_of_attempts = models.IntegerField()

class Admin(models.Model):
    admin_name = models.CharField(max_length=100)

class Category(models.Model):
    category_name = models.CharField(max_length=100)

class QuizDetails(models.Model):
    description = models.CharField(max_length=1000)
    quiz_name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, related_name="quizzes", on_delete=models.CASCADE)
    admin = models.ForeignKey(Admin, related_name="quizzes", on_delete=models.CASCADE)
    time = models.CharField(max_length=100)
    
class Questionnaire(models.Model):
    questions = models.CharField(max_length=10000)
    option1 = models.CharField(max_length=10000,blank=True)
    option2 = models.CharField(max_length=10000,blank=True)
    option3 = models.CharField(max_length=10000,blank=True)
    option4 = models.CharField(max_length=10000,blank=True)
    correct_option = models.CharField(max_length=10000)
    category = models.ForeignKey(Category, related_name="questions", on_delete=models.CASCADE)
    quiz = models.ForeignKey(QuizDetails, related_name="questions", on_delete=models.CASCADE)

class Result(models.Model):
    student_name = models.CharField(max_length=100)
    quiz = models.ForeignKey(QuizDetails, related_name="results", on_delete=models.CASCADE)
    category = models.ForeignKey(Category, related_name="results", on_delete=models.CASCADE)
    score = models.IntegerField()
