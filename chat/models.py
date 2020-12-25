from django.db import models
from main.models import Instructor, Student, Lesson

class Room(models.Model):
    """Represents chat rooms that users can join"""
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=100)
    slug = models.CharField(max_length=50, unique=True)

    def __str__(self):
        """Returns human-readable representation of the model instance."""
        return self.name

class Widget_form(models.Model):
    instructor  = models.ForeignKey(Instructor, on_delete=models.CASCADE, default=None)
    student     = models.ForeignKey(Student, on_delete=models.CASCADE, default=None)
    lesson      = models.ForeignKey(Lesson, on_delete=models.CASCADE, default=None)
    option1     = models.CharField(max_length=20, default="")
    option2     = models.CharField(max_length=20, default="")
    option3     = models.CharField(max_length=20, default="")
    
    option1_approved = models.BooleanField(default=False)
    option2_approved = models.BooleanField(default=False)
    option3_approved = models.BooleanField(default=False)
    status = models.CharField(max_length=40, default="Pending")
    paid = models.BooleanField(default=False)