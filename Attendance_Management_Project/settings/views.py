from django.shortcuts import render, redirect, get_object_or_404
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
    try:
        if request.user.teacher.is_coordinator:
            role = 'staff'
            rolename = 'Coordinator'
            name = request.user.teacher.name
            subjects = Subject.objects.all()
            teachers = Teacher.objects.all()
        else:
            return redirect('loginview')

    except AttributeError:
        role = 'staff'
        rolename = 'Administrator'
        name = request.user.staff.name
        subjects = Subject.objects.all()
        teachers = Teacher.objects.all()

    classes = ClassModel.objects.all()
    students = Student.objects.all()

    context = {'user_id': user_id,
               'user_name': user_name,
               'role': role,
               'rolename': rolename,
               'name': name,
               'date': today,
               'fdate': formatted_date,
               'subjects': subjects,
               'teachers': teachers,
               'classes': classes,
               'students': students
               }

    return render(request, 'staff/schoolsettings.html', context)

@login_required
def schooldatesettings(request):

    if request.user.is_superuser:
        school_start_date = datetime.strptime(request.POST.get('schoolstartdate'), '%Y-%m-%d')
        school_end_date = datetime.strptime(request.POST.get('schoolenddate'),  '%Y-%m-%d')
        if not SchoolDates.objects.all().exists():
            SchoolDates.objects.create(
                start_date = school_start_date,
                end_date = school_end_date
            )
        elif SchoolDates.objects.all().exists():
            schooldate = SchoolDates.objects.all()
            schooldate.update(start_date = school_start_date,end_date = school_end_date)


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

        excessstudents = AttendanceStudent.objects.filter(date__gt = school_end_date)
        excessstudents.delete()

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
            create_attendance_student()
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
    response = {}

    if not Student.objects.filter(email = email).exists():

        student = Student.objects.create(
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
    create_attendance_student()

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

@login_required
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

@login_required
def addsubject(request):
    name = request.POST.get('name')
    print('created')
    if not Subject.objects.filter(name = name).exists():
        Subject.objects.create(
            name = name
        )
    return JsonResponse({})

@login_required
def addclass(request):
    subject_id = request.POST.get('subject')
    grade = request.POST.get('grade')
    block = request.POST.get('block')
    teacher_id = request.POST.get('teacher')

    subject = get_object_or_404(Subject, pk = subject_id)
    teacher = get_object_or_404(Teacher, pk = teacher_id)

    print(teacher)

    if not ClassModel.objects.filter(grade = grade, subject = subject, block = block).exists():
        classref = ClassModel.objects.create(
                    grade = grade,
                    subject = subject,
                    block = block
                )


        if not TeacherClass.objects.filter(teacherref=teacher, classref=classref).exists():
            TeacherClass.objects.create(
                teacherref=teacher,
                classref=classref
            )




    return JsonResponse({})

@login_required
def modifyclassstudent(request):
    action = request.POST.get('action')
    classref_id = request.POST.get('classref')
    student_id = request.POST.get('student')


    name = ''
    error=''

    if 'add' in action:
        student = get_object_or_404(Student, pk=student_id)
        classref = get_object_or_404(ClassModel, pk=classref_id)
        if not ClassStudent.objects.filter(classref=classref,student=student).exists():

            ClassStudent.objects.create(
                classref = classref,
                student = student
            )
            name = student.name

    elif 'save' in action:
        if (student_id is not '') and (classref_id is not ''):
            student = get_object_or_404(Student, pk=student_id)
            classref = get_object_or_404(ClassModel, pk=classref_id)
            if not ClassStudent.objects.filter(classref=classref, student=student).exists():
                ClassStudent.objects.create(
                    classref=classref,
                    student=student
                )
            name = student.name
        else:
            error = 'Please select a student to add first'

    response = {'student': name, 'error': error}
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

    filepath = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'media/Parent_Data.xlsx')
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
            if not ParentStudent.objects.filter(parentref = parent, studentref = student).exists():

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

def create_attendance_student():
    dates = SchoolDates.objects.all()[:1].get()
    end_date = dates.end_date

    students = Student.objects.all()

    date_now = date.today()

    days = int((end_date - date_now).days) + 1

    for i in range(days):
        for student in students:
            currentday = date_now + timedelta(days=i)
            if not AttendanceStudent.objects.filter(date=currentday, studentref=student).exists():
                AttendanceStudent.objects.create(
                    studentref=student,
                    studentref_name=student.name,
                    studentref_grade=student.grade,
                    attendance=False,
                    date=currentday
                )