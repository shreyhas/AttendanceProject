from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from account.models import TeacherClass
from .models import *
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


    context = {
        'class_id': class_id,
        'class_name': class_name,
        'teacher_name': teacher_name,
        'id': id,
        'classstudents': classstudents,
        'name': name,
        'rolename': rolename,
        'user_id': user_id,
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
        else:
            sc.attendance = False
        sc.save()

    return redirect('classview')