from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import auth
from django.http.response import JsonResponse
from django.contrib.auth.decorators import login_required
from account.models import Teacher
from .models import *
from classes.models import *
from django.core.mail import send_mail
import random

def login(request):

    if request.method == 'POST':
        user = auth.authenticate(
            username = request.POST['uname'],
            password = request.POST['psw']
        )
        if user is not None:
            auth.login(request,user)
            return redirect('loginview')
        else:
            error = 'User not found'
            context = {
                'error': error
            }
            return render(request, "login/LoginPage.html", context)
    return render(request, "login/LoginPage.html")

@login_required
def logout(request):
    auth.logout(request)
    return redirect('home')
# Create your views here.

def requests(request):


    teacher_list = []
    for teacher in Teacher.objects.all():
        if teacher.is_coordinator:
            teacher_list.append(teacher)

    print(teacher_list)
    context = {
        'teacher': teacher_list
    }
    return render(request, 'login/requests.html', context)

def verifyemail(request):
    email = request.POST.get('email')

    parents = Parent.objects.filter(email = email)
    response = {}

    if (len(list(parents))>0):
        otp = random.randrange(100000, 1000000, 1)
        print(otp)
        response['result'] = True
        response['message'] = 'E-Mail ID verified'
        send_mail(
            subject='Access Code for Request',
            message=f'Your access code is {otp}',
            from_email='fyberboard@gmail.com',
            recipient_list=[email],
            fail_silently=False
        )
        OTPVerification.objects.create(
            parentemail = email,
            otpcode=otp,
        )
    else:
        response['result'] = False
        response['message'] = 'E-Mail ID not registered'
    return JsonResponse(response)

def verifyotp(request):


    email = request.POST.get('email')
    otp = request.POST.get('otp')
    response = {}

    otpverify = OTPVerification.objects.filter(
        parentemail = email,
        response = -1
    )
    for ov in otpverify:
        if ov.otpcode == int(otp):
            ov.response = otp
            ov.save()
            response['result'] = True

            parent = Parent.objects.filter(email = email)[:1]
            parentstudents = ParentStudent.objects.filter(parentref = parent)
            students = []
            for ps in parentstudents:
                students.append((ps.studentref.id, ps.studentref.name, ps.studentref.grade))
            response['students'] = list(students)

        else:
            response['result'] = False

    return JsonResponse(response)

def parentrequest(request):

    parentemail = request.POST.get('parentemail')
    requestselect = request.POST.get('selectrequest')
    studentselect = request.POST.get('studentselectradio')
    coordinatorselect = request.POST.get('coordinatorselect')

    student = get_object_or_404(Student, pk = studentselect)
    coordinator = get_object_or_404(Teacher, pk = coordinatorselect)

    ParentRequest.objects.create(
        parent_email = parentemail,
        studentref = student,
        coordinatorref = coordinator,
        request_type = requestselect
    )

    context = {
        'message': "Your request has been submitted"
    }

    return render(request, 'login/LoginPage.html', context)