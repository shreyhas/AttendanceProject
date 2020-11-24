from django.shortcuts import render, redirect
from datetime import date, datetime
import csv
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from account.models import TeacherClass
from classes.models import *
# Create your views here.
@login_required
def loginview(request):
    user_id = request.user.id
    user_name = request.user
    role = None
    today = date.today()
    attendancestudent = None
    classes = None
    formatted_date = datetime.today().strftime('%Y-%m-%d')
    try:
        if request.user.teacher is not None:
            role = 'teacher'
            rolename = 'Teacher'
            name = request.user.teacher.name
            classes = TeacherClass.objects.filter(teacherref = request.user.teacher)
    except AttributeError:
        role = 'staff'
        rolename = 'Administrator'
        name = request.user.staff.name
        attendancestudent = AttendanceStudent.objects.filter(date = today)

    context = {'user_id': user_id,
               'user_name': user_name,
               'role': role,
               'rolename': rolename,
               'name': name,
               'classes': classes,
               'date': today,
               'fdate': formatted_date,
               'attendancestudents': attendancestudent
               }
    if role is 'staff':
        return render(request, 'staff/staffview.html', context)

    else:
        return render(request, 'staff/teacherview.html', context)

@login_required
def classview(request):

    user_id = request.user.id
    today = date.today()
    user_name = request.user
    try:
        if request.user.teacher is not None:
            name = request.user.teacher.name
            attendancestudent = None
    except AttributeError:
        role = 'staff'
        rolename = 'Administrator'
        classes = TeacherClass.objects.all()
        name = request.user.staff.name


    context = {
        'name': name,
        'rolename':rolename,
        'user_id': user_id,
        'date': today,
        'user_name': user_name,
        'role': role,
        'classes': classes,

    }

    return render(request, 'staff/classview.html', context)

@login_required
def record(request):
    marked = request.POST.getlist('attendance')
    print(marked)

    for i in range(len(marked)):
        marked[i] = int(marked[i])

    students = AttendanceStudent.objects.all()
    for student in students:
        if student.studentref.id in marked:
            present_absent = True
        else:
            present_absent = False

        student.attendance = present_absent
        student.save()


    return redirect('loginview')

@login_required
def changedate(request):

    date_selected = request.POST.get('date')
    print(date_selected)

    user_id = request.user.id
    today = date.today()

    try:
        if request.user.teacher is not None:
            name = request.user.teacher.name
            attendancestudent = None
    except AttributeError:
        rolename = 'Administrator'
        name = request.user.staff.name
        attendancestudent = AttendanceStudent.objects.filter(date = date_selected)

    #attendancestudent = list(attendancestudent)

    for student in attendancestudent:
        #print(student.studentref.name)
        student.studentref_name = student.studentref.name
        student.studentref_grade = student.studentref.grade
        student.save()

    context = {
        'attendancestudents': list(attendancestudent.values()),
        'name': name,
        'rolename': rolename,
        'user_id': user_id,
        'date': today,
    }


    return JsonResponse(context)

def changegrade(request):

    grade_selected = request.POST.get('grade')
    print(grade_selected)

    user_id = request.user.id
    today = date.today()

    date_selected = request.POST.get('date')
    print(date_selected)

    user_id = request.user.id
    today = date.today()

    try:
        if request.user.teacher is not None:
            name = request.user.teacher.name
            attendancestudent = None
    except AttributeError:
        name = request.user.staff.name
        rolename = 'Administrator'
        name = request.user.staff.name

        if grade_selected == 13:
            attendancestudent = AttendanceStudent.objects.all(date=date_selected)
        else:
            attendancestudent = AttendanceStudent.objects.filter(
                studentref_grade=grade_selected,
                date=date_selected
            )



        print(attendancestudent)
    #attendancestudent = list(attendancestudent)

    for student in attendancestudent:
        #print(student.studentref.name)
        student.studentref_name = student.studentref.name
        student.studentref_grade = student.studentref.grade
        student.save()

    context = {
        'attendancestudents': list(attendancestudent.values()),
        'name': name,
        'rolename': rolename,
        'user_id': user_id,
        'date': today,
    }


    return JsonResponse(context)

def export(request):

   response = HttpResponse(content_type='text/csv')
   response['Content-Disposition'] = 'export.csv'
   writer = csv.writer(response)
   writer.writerow(['1', '2', '3'])
   writer.writerow(['4', '5', '6'])

   return response
