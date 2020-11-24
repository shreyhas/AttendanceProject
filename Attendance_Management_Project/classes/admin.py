from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Student)
admin.site.register(ClassModel)
admin.site.register(Subject)
admin.site.register(ClassStudent)
admin.site.register(AttendanceStudent)
