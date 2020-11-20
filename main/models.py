from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
from datetime import datetime

class User(AbstractUser):
    Id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    age = models.IntegerField(default=0)
    blocked = models.BooleanField(default=False)
    img = models.ImageField(upload_to='media', default='default.png')
    last_login = models.CharField(max_length = 30)
    email = models.EmailField()
    password = models.CharField(max_length=20)
    username = models.CharField(default=email, max_length=200, unique=True)
    intro_msg = models.CharField(max_length = 200)
    catch_phrase = models.CharField(max_length = 200)

class Instructor(User):
    what_you_can_ask_for = models.CharField(max_length = 200)
    field = models.CharField(max_length=100)
    number_of_ratings = models.IntegerField(default=0)
    total_ratings = models.IntegerField(default=0)
    rating = models.IntegerField(default=  0)
    paypal_account = models.CharField(max_length=500)

class Student(User):
    what_I_want_to_talk_about = models.CharField(max_length=200)

class Lesson(models.Model):
    title = models.CharField(max_length=50)
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE, default=None)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, default=None, null=True)
    Date = models.DateTimeField()
    lesson_type = models.CharField(max_length=20)
    starting = models.CharField(max_length=20, default='None')
    ending = models.CharField(max_length=20, default='None')
    date_to_display = models.CharField(max_length=20, default='None')
    rating = models.FloatField(default=5)
    day = models.CharField(max_length=50, default ="None")