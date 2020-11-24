from django.db import models
from classes.models import ClassModel
from django.contrib.auth.models import User

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    phone = models.CharField(max_length=12)
    email = models.CharField(max_length=60)

    def __str__(self):
        return f'{self.name}'

class TeacherClass(models.Model):
    teacherref = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    classref = models.ForeignKey(ClassModel, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.teacherref} for {self.classref}'

class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    phone = models.CharField(max_length=12)
    email = models.CharField(max_length=60)

    def __str__(self):
        return f'{self.name}'
