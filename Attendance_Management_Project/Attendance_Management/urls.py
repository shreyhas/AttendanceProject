"""Attendance_Management URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

import home.views
import login.views
import staff.views
import classes.views
import settings.views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home.views.home, name ='home'),
    path('login/', login.views.login, name ="login"),
    path('logout/', login.views.logout, name ="logout"),
    path('requests/', login.views.requests, name = "requests"),
    path('verifyemail/', login.views.verifyemail, name = "verifyemail"),
    path('verifyotp/', login.views.verifyotp, name = "verifyotp"),
    path('parentrequest/', login.views.parentrequest, name = "parentrequest"),
    path('staff/', staff.views.loginview, name ="loginview"),
    path('classdetails/<int:class_id>/<int:teacherclass_id>', classes.views.classdetails, name="classdetails"),
    path('save/<int:class_id>', classes.views.save, name="save"),
    path('record/', staff.views.record, name="record"),
    path('staff/classview/', staff.views.classview, name="classview"),
    path('securityview/', staff.views.securityview, name="securityview"),
    path('authorizerequest/', staff.views.authorizerequest, name="authorizerequest"),
    path('changedate/', staff.views.changedate, name="changedate"),
    path('changegrade/', staff.views.changegrade, name="changegrade"),
    path('export/', staff.views.export, name="export"),
    path('updaterequest/', staff.views.updaterequest, name="updaterequest"),
    path('notifications/', staff.views.notifications, name="notifications"),
    path('staff/schoolsettings/', settings.views.schoolsettings, name='schoolsettings'),
    path('schooldatesettings/', settings.views.schooldatesettings, name='schooldatesettings'),
    path('importstudents/', settings.views.importstudents, name='importstudents'),
    path('importparents/', settings.views.importparents, name='importparents'),
    path('importteachers/', settings.views.importteachers, name='importteachers'),
    path('addparent/', settings.views.addparent, name='addparent'),
    path('addstudent/', settings.views.addstudent, name='addstudent'),
    path('addstaff/', settings.views.addstaff, name='addstaff'),
    path('addsubject/', settings.views.addsubject, name='addsubject'),
    path('addclass/', settings.views.addclass, name='addclass'),
    path('modifyclassstudent/', settings.views.modifyclassstudent, name='modifyclassstudent'),

]
