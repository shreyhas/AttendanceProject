from django.shortcuts import render, redirect
from datetime import date, datetime, timedelta
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from account.models import *
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
    rolename = None
    name = None
    today = date.today()

    formatted_date = datetime.today().strftime('%Y-%m-%d')
    if request.user.is_superuser:
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

        return render(request, 'staff/schoolsettings.html', context)
    else:
        return redirect('loginview')

@login_required
def schooldatesettings(request):

    if request.user.is_superuser:
        school_start_date = datetime.strptime(request.POST.get('schoolstartdate'), '%Y-%m-%d')
        school_end_date = datetime.strptime(request.POST.get('schoolenddate'),  '%Y-%m-%d')
        students = Student.objects.filter(active = True)

        days = int((school_end_date-school_start_date).days) + 1

        for i in range(days):
            currentday = school_start_date + timedelta(days = i)
            for student in students:
                #create students with date

                if not AttendanceStudent.objects.filter(date = currentday, studentref = student).exists():
                    AttendanceStudent.objects.create(
                        studentref = student,
                        studentref_name = student.name,
                        studentref_grade = student.grade,
                        attendance = False,
                        date = currentday
                    )

        return redirect('schoolsettings')
    else:
        return redirect('loginview')

@login_required
def importstudents(request):

    if request.user.is_superuser:

        if request.FILES.get('studentdata'):

            student_data_file = request.FILES.get('studentdata')
            fs = FileSystemStorage()
            if fs.exists('Student_Data.xlsx'):
                fs.delete('Student_Data.xlsx')
                fs.save('Student_Data.xlsx', student_data_file)
            else:
                fs.save('Student_Data.xlsx', student_data_file)

            load_student_data()

        return redirect('schoolsettings')
    else:
        return redirect('loginview')

@login_required
def importparents(request):

    if request.user.is_superuser:

        if request.FILES.get('parentdata'):

            parent_data_file = request.FILES.get('parentdata')
            fs = FileSystemStorage()
            if fs.exists('Parent_Data.xlsx'):
                fs.delete('Parent_Data.xlsx')
                fs.save('Parent_Data.xlsx', parent_data_file)
            else:
                fs.save('Parent_Data.xlsx', parent_data_file)

            load_parent_data()
            create_parent_student()

        return redirect('schoolsettings')
    else:
        return redirect('loginview')

@login_required
def importteachers(request):

    if request.user.is_superuser:

        if request.FILES.get('teacherdata'):

            teacher_data_file = request.FILES.get('teacherdata')
            fs = FileSystemStorage()
            if fs.exists('Teacher_Data.xlsx'):
                fs.delete('Teacher_Data.xlsx')
                fs.save('Teacher_Data.xlsx', teacher_data_file)
            else:
                fs.save('Teacher_Data.xlsx', teacher_data_file)

            load_teacher_data()

        return redirect('schoolsettings')
    else:
        return redirect('loginview')

@login_required
def addstudent(request):

    name = request.POST.get('name')
    grade = request.POST.get('grade')
    phone = request.POST.get('phone')
    email = request.POST.get('email')
    femail = request.POST.get('femail')
    memail = request.POST.get('memail')

    if not Student.objects.filter(email = email).exists():

        Student.objects.create(
            name = name,
            grade = grade,
            phone = phone,
            email = email,
            fathers_email = femail,
            mothers_email = memail,
        )
    else:
        response['message'] = 'Student already exists'
    create_parent_student()

    response={}

    return JsonResponse(response)

@login_required
def addparent(request):

    name = request.POST.get('name')
    email = request.POST.get('email')

    if not Parent.objects.filter(email = email).exists():

        Parent.objects.create(
            name = name,
            email = email,
        )
    else:
        response['message'] = 'Parent already exists'
    create_parent_student()

    response={}

    return JsonResponse(response)

def addstaff(request):
    if request.user.is_superuser:
        stafftype = request.POST.get('stafftype')
        print(type(stafftype))
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        coordinator = request.POST.get('coordinator')
        if 'Y' in coordinator:
            bool = True
        else:
            bool = False
        password = request.POST.get('password')
        grades = request.POST.get('grades')


        user = User.objects.create_user(
            username=email,
            password=password,
            email=email
        )
        user.save()

        if 'admin' in stafftype:
            print('Yes')
            if not Staff.objects.filter(email = email).exists():
                print('Yes')
                Staff.objects.create(
                    user=user,
                    name=name,
                    phone=phone,
                    email=email,
                )
        elif 'teacher' in stafftype:
            if not Teacher.objects.filter(email = email).exists():
                Teacher.objects.create(
                    user=user,
                    name=name,
                    phone=phone,
                    email=email,
                    is_coordinator=bool,
                    grades=grades
                )

    response = {}
    return JsonResponse(response)


def load_student_data():

    filepath = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'media/Student_Data.xlsx')
    for grade in range(13):
        if grade == 0:
            grade = 'KG'
        studentdata = pd.read_excel(filepath, sheet_name = f'Grade {grade}')
        df = pd.DataFrame(studentdata)

        for row in df.iterrows():
            print(row)
            series = row[1]
            print(series)
            Name = series[0]
            Phone = 1234567890
            Email = 'example@domain.com'
            FEmail = series[3]
            MEmail = series[4]
            if not Student.objects.filter(name = Name, email = Email).exists():
                Student.objects.create(
                    name = Name,
                    phone = Phone,
                    email = Email,
                    grade = grade,
                    fathers_email = FEmail,
                    mothers_email = MEmail
                )

def load_parent_data():

    filepath = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'media  /Parent_Data.xlsx')
    parentdata = pd.read_excel(filepath)
    df = pd.DataFrame(parentdata)

    for row in df.iterrows():
        series = row[1]

        Name = series[0]
        Email = series[1]

        if not Parent.objects.filter(name=Name,email=Email).exists():
            Parent.objects.create(
                name = Name,
                email = Email
            )

def create_parent_student():
    for parent in Parent.objects.all():
        students = Student.objects.filter(fathers_email = parent.email) | Student.objects.filter(mothers_email = parent.email)
        for student in students:
            ParentStudent.objects.create(
                parentref = parent,
                studentref = student
            )

def load_teacher_data():

    filepath = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'media/Teacher_Data.xlsx')
    teacherdata = pd.read_excel(filepath)
    df = pd.DataFrame(teacherdata)

    for row in df.iterrows():
        series = row[1]
        Name = series[0]
        Phone = series[1]
        Email = series[2]
        is_coordinator = str(series[3])
        if 'Y' in is_coordinator:
            bool = True
        else:
            bool = False
        Grades = series[4]
        Password = series[5]

        user = User.objects.create_user(
            username=Email,
            password=Password,
            email=Email
        )
        user.save()

        Teacher.objects.create(
            user = user,
            name = Name,
            phone = Phone,
            email = Email,
            is_coordinator = bool,
            grades = Grades
        )


    pass