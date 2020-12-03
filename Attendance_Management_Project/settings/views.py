from django.shortcuts import render, redirect
from datetime import date, datetime, timedelta
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from account.models import TeacherClass
from .models import *
from classes.models import *
from login.models import *
import os
import pandas as pd

# Create your views here.
@login_required
def schoolsettings(request):
    user_id = request.user.id
    user_name = request.user
    role = None
    today = date.today()

    formatted_date = datetime.today().strftime('%Y-%m-%d')
    if request.user.staff is not None:
        role = 'staff'
        rolename = 'Administrator'
        name = request.user.staff.name

    context = {'user_id': user_id,
               'user_name': user_name,
               'role': role,
               'rolename': rolename,
               'name': name,
               'date': today,
               'fdate': formatted_date,
               }

    return render(request, 'staff/schoolsettings.html')

@login_required
def importstudents(request):

    if request.user.staff is not None:
        load_student_data()

    else:
        return redirect('loginview')

    return JsonResponse({})

def load_student_data():

    filepath = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static/schooldata/Student Data.xlsx')
    for grade in range(13):
        if grade == 0:
            grade = 'KG'
        studentdata = pd.read_excel(filepath, sheet_name = f'Grade {grade}')
        df = pd.DataFrame(studentdata)

        for row in df.iterrows():
            series = row[1]
            Name = series[0]
            Phone = 1234567890
            Email = 'example@domain.com'
            Student.objects.create(
                name = Name,
                phone = Phone,
                email = Email,
                grade = grade
            )

def load_teacher_data():

    filepath = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static/schooldata/Student Data.xlsx')
    for grade in range(13):
        if grade == 0:
            grade = 'KG'
        studentdata = pd.read_excel(filepath, sheet_name = f'Grade {grade}')
        df = pd.DataFrame(studentdata)

        for row in df.iterrows():
            series = row[1]
            Name = series[0]
            Phone = 1234567890
            Email = 'example@domain.com'
            Student.objects.create(
                name = Name,
                phone = Phone,
                email = Email,
                grade = grade
            )
