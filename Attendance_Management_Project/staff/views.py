from django.shortcuts import render, redirect
from datetime import date, datetime
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from account.models import TeacherClass
from classes.models import *
from login.models import *

import io
from xlsxwriter.workbook import Workbook

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
            if request.user.teacher.is_coordinator:
                role = 'staff'
                rolename = 'Coordinator'
                grades = request.user.teacher.grades.split(',')
                for i in range(len(grades)):
                    grades[i] = int(grades[i])
                attendancestudent = AttendanceStudent.objects.filter(studentref_grade__in = grades, date = today)
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
    formatted_date = datetime.today().strftime('%Y-%m-%d')
    try:
        if request.user.teacher is not None:
            name = request.user.teacher.name
            attendancestudent = None
            if request.user.teacher.is_coordinator:
                role = 'staff'
                rolename = 'Coordinator'
                grades = request.user.teacher.grades.split(',')
                for i in range(len(grades)):
                    grades[i] = int(grades[i])
                classes = TeacherClass.objects.filter(teacherref = request.user.teacher)
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
        'fdate': formatted_date

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
            if request.user.teacher.is_coordinator:
                rolename = 'Coordinator'
                name = request.user.teacher.name
                grades = request.user.teacher.grades.split(',')
                for i in range(len(grades)):
                    grades[i] = int(grades[i])
                attendancestudent = AttendanceStudent.objects.filter(
                    date=date_selected,
                    studentref_grade__in = grades
                )
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

@login_required
def changegrade(request):

    grade_selected = request.POST.get('grade')

    user_id = request.user.id
    today = date.today()
    grade_selected = int(grade_selected)

    date_selected = request.POST.get('date')

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

def changeclassgrade(request):

    grade_selected = request.POST.get('grade')
    pass

@login_required
def export(request):

    date_selected = request.POST.get('selectdate')
    grade_selected = request.POST.getlist('grade-select')
    print(type(grade_selected))

    for i in range(len(grade_selected)):
        grade_selected[i] = int(grade_selected[i])

    print(date_selected, grade_selected)


    try:
        if request.user.teacher is not None:
            pass
    except AttributeError:

        attendancestudent = AttendanceStudent.objects.filter(
            studentref_grade__in=grade_selected,
            date=date_selected
        )
        print(attendancestudent)

    #create and fill dict with grade-wise data
    studentdict = {}
    for student in attendancestudent:

        if student.attendance:
            present_absent = 'Present'
        else:
            present_absent = 'Absent'

        if student.studentref.grade in studentdict:
            # [id,name,grade,email,attendance]
            studentdict[student.studentref.grade].append((
                student.studentref.id,
                student.studentref.name,
                student.studentref.grade,
                student.studentref.email,
                present_absent,
            ))
        else:
            studentdict[student.studentref.grade] = [(
                student.studentref.id,
                student.studentref.name,
                student.studentref.grade,
                student.studentref.email,
                present_absent,
            )]

    print (studentdict)
    output = io.BytesIO()
    workbook = Workbook(output, {'in_memory': True})
    bold = workbook.add_format({'bold': True})

    for grade in studentdict:
        attendance = studentdict[grade]
        # [id,name,grade,email,attendance]

        worksheet = workbook.add_worksheet(f'Grade {grade}')
        worksheet.write(0,0, 'ID', bold)
        worksheet.write(0,1, 'Name', bold)
        worksheet.write(0,2, 'Grade', bold)
        worksheet.write(0,3, 'Email', bold)
        worksheet.write(0,4, 'Attendance', bold)
        for i in range(len(attendance)):
            student = attendance[i]
            for j in range(len(student)):
                worksheet.write(i+1,j, student[j])

    workbook.close()
    output.seek(0)

    response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = f"attachment; filename=export_{date_selected}.xlsx"

    output.close()

    return response

