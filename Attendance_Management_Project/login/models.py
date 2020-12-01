from django.db import models
from classes.models import Student
from datetime import datetime
from account.models import Teacher

class Parent(models.Model):
    name = models.CharField(max_length=20)
    email = models.EmailField()

    def __str__(self):
        return f'{self.name}'

class ParentStudent(models.Model):
    parentref = models.ForeignKey(Parent, on_delete=models.CASCADE)
    studentref = models.ForeignKey(Student, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.parentref.name} is parent of {self.studentref.name}'

class OTPVerification(models.Model):
    parentemail = models.EmailField(null=True)
    otpcode = models.IntegerField()
    date_time = models.DateTimeField(default=datetime.now())
    response = models.IntegerField(default=-1)

class ParentRequest(models.Model):
    parent_email = models.EmailField()
    studentref = models.ForeignKey(Student, on_delete=models.CASCADE)
    coordinatorref = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    request_type = models.CharField(max_length=20)
    date = models.DateField(default=datetime.today(), null = True)
    approved_by_coordinator = models.BooleanField(default=False)
    viewed_by_coordinator = models.BooleanField(default=False)
    approved_by_staff = models.BooleanField(default=False)
    viewed_by_staff = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.parent_email}, {self.studentref.name}, {self.coordinatorref.name}'




