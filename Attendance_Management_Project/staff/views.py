from django.shortcuts import render, redirect, get_object_or_404
from datetime import date, datetime, timedelta
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.models import User
from account.models import TeacherClass
from django.core.mail import send_mail
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
    requests = None
    formatted_date = datetime.today().strftime('%Y-%m-%d')
    present_as = 0
    absent_as = 0
    disabled = False
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
                attendancestudent = AttendanceStudent.objects.filter(studentref_grade__in = grades, date = today).order_by('studentref_name')
                #if datetime.now()>
                requests = ParentRequest.objects.filter(
                    coordinatorref = request.user.teacher,
                    viewed_by_coordinator = False
                )


    except AttributeError:
        role = 'staff'
        rolename = 'Administrator'
        name = request.user.staff.name
        attendancestudent = AttendanceStudent.objects.filter(date = today).order_by('studentref_name')
        if request.user.staff.verify_permissions:
            requests = ParentRequest.objects.filter(
                approved_by_coordinator=True,
                viewed_by_staff=False,
                request_type='gatepass',
                date=date.today()
            )
    present_as, absent_as, leave = present_absent_as(attendancestudent)

    context = {'user_id': user_id,
               'user_name': user_name,
               'role': role,
               'rolename': rolename,
               'name': name,
               'classes': classes,
               'date': today,
               'fdate': formatted_date,
               'attendancestudents': attendancestudent,
               'present': present_as,
               'absent': absent_as,
               'leave': leave,
               'requests': requests
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
            role = 'teacher'
            rolename = 'Teacher'
            name = request.user.teacher.name
            classes = TeacherClass.objects.filter(teacherref=request.user.teacher)
            attendancestudent = None
            if request.user.teacher.is_coordinator:
                role = 'staff'
                rolename = 'Coordinator'
                grades = request.user.teacher.grades.split(',')
                for i in range(len(grades)):
                    grades[i] = int(grades[i])
                classrefs = ClassModel.objects.filter(grade__in = grades)
                classes = TeacherClass.objects.filter(classref__in = classrefs)
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
def securityview(request):

    requests = ParentRequest.objects.filter(
        approved_by_staff = True,
        approved_by_coordinator = True,
        request_type = 'gatepass',
        date = date.today()
    )
    print(requests)
    context = {'requests': requests}

    return render(request, 'staff/securityview.html', context)

@login_required
def authorizerequest(request):
    request_id = request.POST.get('request_id')
    requestref = get_object_or_404(ParentRequest, pk=request_id)

    requestref.delete()


    return JsonResponse({'request_id':request_id})

@login_required
def record(request):
    marked = request.POST.getlist('attendance')
    date = request.POST.get('datepicker')
    print(marked)

    for i in range(len(marked)):
        marked[i] = int(marked[i])

    students = AttendanceStudent.objects.filter(date = date)
    for student in students:
        if student.studentref.id in marked:
            present_absent = True
        else:
            present_absent = False
            parentstudents = ParentStudent.objects.filter(studentref = student.studentref)
            to_emails = []
            for ps in parentstudents:
                to_emails.append(ps.parentref.email)
            send_mail(
                subject=f'Student Attendance: {student.studentref.name}',
                message=f'Your student, {student.studentref.name} was marked absent for the day',
                from_email='fyberboard@gmail.com',
                recipient_list=to_emails,
                fail_silently=False
            )

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

    present_as, absent_as, leave = present_absent_as(attendancestudent)

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
        'present': present_as,
        'absent': absent_as,
        'leave': leave
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
            if request.user.teacher.is_coordinator:
                rolename = 'Coordinator'
                grades = request.user.teacher.grades.split(',')
                for i in range(len(grades)):
                    grades[i] = int(grades[i])
                if grade_selected == 13:
                    attendancestudent = AttendanceStudent.objects.filter(studentref_grade__in=grades, date=date_selected).order_by('studentref_name')
                else:
                    attendancestudent = AttendanceStudent.objects.filter(studentref_grade__in=grades, date=date_selected) & AttendanceStudent.objects.filter(studentref_grade=grade_selected, date=date_selected)



    except AttributeError:
        name = request.user.staff.name
        rolename = 'Administrator'
        name = request.user.staff.name

        if grade_selected == 13:
            attendancestudent = AttendanceStudent.objects.filter(date=date_selected)
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

    present_as, absent_as, leave = present_absent_as(attendancestudent)

    context = {
        'attendancestudents': list(attendancestudent.values()),
        'name': name,
        'rolename': rolename,
        'user_id': user_id,
        'date': today,
        'present': present_as,
        'absent': absent_as,
        'leave': leave
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

@login_required
def notifications(request):

    rolename = request.POST.get('rolename')

    userobj = request.user

    if 'Administrator' in rolename:
        staff = userobj.staff
        if staff.verify_permissions:
            requests = ParentRequest.objects.filter(
                approved_by_coordinator=True,
                viewed_by_staff=False,
                request_type='gatepass',
            )
    elif 'Coordinator' in rolename:
        requests = ParentRequest.objects.filter(
            coordinatorref=request.user.teacher,
            viewed_by_coordinator=False,
        )

    studentinfo = []

    for requestref in requests:
        student_name = requestref.studentref.name
        student_grade = requestref.studentref.grade
        studentinfo.append((student_name,student_grade))

    response  = {
        'requests': list(requests.values()),
        'studentinfo': studentinfo
    }

    return JsonResponse(response)

@login_required
def updaterequest(request):
    rolename = request.POST.get('rolename')
    approved = request.POST.get('approved')
    if 'true' in approved:
        approved = True
    else:
        approved = False
    request_id = request.POST.get('request_id')

    parentrequest = get_object_or_404(ParentRequest, pk=request_id)
    request_type = parentrequest.request_type
    date = parentrequest.date
    studentref = parentrequest.studentref

    if 'gatepass' in request_type:
        if 'Coordinator' in rolename:
            if approved:
                parentrequest.approved_by_coordinator = True
                parentrequest.viewed_by_coordinator = True
                parentrequest.save()
            else:
                parentrequest.delete()
        elif 'Administrator' in rolename:
            if approved:
                parentrequest.approved_by_staff = True
                parentrequest.viewed_by_staff = True
                parentrequest.save()
            else:
                parentrequest.delete()
    if 'leaverequest' in request_type:
        if 'Coordinator' in rolename:
            if approved:
                parentrequest.approved_by_coordinator = True
                parentrequest.viewed_by_coordinator = True
                parentrequest.save()
                student_on_leave(studentref, date)

            else:
                parentrequest.delete()


    return JsonResponse({'id':request_id})

def present_absent_as(attendancestudent):
    present_as = 0
    absent_as = 0
    leave = 0

    if attendancestudent:

        for student in attendancestudent:
            print(student.attendance)
            if student.attendance == True:
                present_as += 1
            else:
                if student.on_leave:
                    leave +=1
                else:
                    absent_as += 1
        print(present_as,absent_as)

    return present_as,absent_as,leave

def student_on_leave(studentref, date):
    student = AttendanceStudent.objects.filter(
        studentref = studentref,
        date = date
    )
    classstudent = ClassStudent.objects.filter(
        student = studentref,
        date = date
    )
    student.update(on_leave = True)
    classstudent.update(on_leave = True)

# @periodic_task(
#     run_every=(crontab(minute='*/15')),
#     name="task_generate_class_students",
#     ignore_result=True
# )
def task_generate_class_students():

    pass

def generate_class_students():
    pass