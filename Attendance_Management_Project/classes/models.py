from django.db import models
from datetime import datetime


class Student(models.Model):
    name = models.CharField(max_length=30)
    phone = models.IntegerField()
    email = models.CharField(max_length=100)
    grade = models.IntegerField()
    active = models.BooleanField(null=True, default=True)

    def __str__(self):
        return f'{self.name} {self.grade}'

class Subject(models.Model):
    name = models.CharField(max_length=15)

    def __str__(self):
        return f'{self.name}'

class ClassModel(models.Model):
    grade = models.IntegerField()
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.subject} for grade {self.grade}'

class ClassStudent(models.Model):
    classref = models.ForeignKey(ClassModel, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    attendance = models.BooleanField(default=False)
    date = models.DateField(default=datetime.today(), null=True)
    on_leave = models.BooleanField(null = True, default=False)
    def __str__(self):
        return f'{self.student} in {self.classref}'

class AttendanceStudent(models.Model):
    studentref = models.ForeignKey(Student, on_delete=models.CASCADE)
    studentref_name = models.CharField(max_length=30)
    studentref_grade = models.IntegerField(default=12)
    attendance = models.BooleanField()
    date = models.DateField(default=datetime.today())
    on_leave = models.BooleanField(null=True, default=False)
    def __present_absent__(self):
        if self.attendance is True:
            present_absent = 'Present'
        else:
            present_absent = 'Absent'
        return present_absent

    def __str__(self):
        return f'{self.studentref.name} is {self.__present_absent__()}'