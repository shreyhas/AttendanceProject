from django.db import models
from classes.models import ClassModel
from django.contrib.auth.models import User

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    phone = models.CharField(max_length=12)
    email = models.CharField(max_length=60)
    is_coordinator = models.BooleanField(default=False, help_text="Select only if Teacher is Coordinator.")
    grades = models.CharField(max_length=15, null = True, help_text ="Separate grades by commas.")

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
    verify_permissions = models.BooleanField(null=True, default=False)

    def __str__(self):
        return f'{self.name}'

class Security(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
