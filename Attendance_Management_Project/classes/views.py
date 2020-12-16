from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from account.models import TeacherClass
from django.core.mail import send_mail
from .models import *
from login.models import *
# Create your views here.

@login_required
def classdetails(request, class_id, teacherclass_id):
    id = request.user.id
    teacherclass = get_object_or_404(TeacherClass, pk = teacherclass_id)
    teacher_name = teacherclass.teacherref.name
    class_name = teacherclass.classref
    classstudents = ClassStudent.objects.filter(classref = class_id)

    user_id = request.user.id
    try:
        if request.user.teacher is not None:
            rolename = 'Teacher'
            name = request.user.teacher.name
    except AttributeError:
        rolename = 'Administrator'
        name = request.user.staff.name

    present, absent = present_absent_cs(classstudents)
    context = {
        'class_id': class_id,
        'class_name': class_name,
        'teacher_name': teacher_name,
        'id': id,
        'classstudents': classstudents,
        'name': name,
        'rolename': rolename,
        'user_id': user_id,
        'present': present,
        'absent': absent
    }
    return render(request, 'classes/classdetails.html', context)

@login_required
def save(request, class_id):
    marked = request.POST.getlist('attendance')

    for i in range(len(marked)):
        marked[i] = int(marked[i])

    studentclasses = ClassStudent.objects.filter(classref = class_id)
    for sc in studentclasses:
        if sc.student.id in marked:
            sc.attendance = True
            if sc.is_homeroomclassstudent:
                studentref = sc.student
                attendancestudent = AttendanceStudent.objects.filter(date=sc.date, studentref=studentref)
                attendancestudent.update(attendance=True)
        else:
            sc.attendance = False
            if sc.is_homeroomclassstudent:
                studentref = sc.student
                attendancestudent = AttendanceStudent.objects.filter(date=sc.date, studentref=studentref)
                attendancestudent.update(attendance=False)
            student = sc
            parentstudents = ParentStudent.objects.filter(studentref=student.student)
            to_emails = []
            for ps in parentstudents:
                to_emails.append(ps.parentref.email)
            send_mail(
                subject=f'Student Attendance: {student.student.name}',
                message=f'Your student, {student.student.name} was marked absent for the class {sc.classref}',
                from_email='fyberboard@gmail.com',
                recipient_list=to_emails,
                fail_silently=False
            )

        sc.save()

    return redirect('classview')

def present_absent_cs(classstudents):
    present = 0
    absent = 0
    for student in classstudents:
        if student.attendance:
            present += 1
        else:
            absent += 1

    return present, absent