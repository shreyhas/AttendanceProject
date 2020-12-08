from django.db import models

# Create your models here.
class StudentDataFileUpload(models.Model):
    title = models.CharField(max_length=30, default='StudentData')
    file = models.FileField(upload_to='static/schooldata')
    upload_date_time = models.DateTimeField(null=True)

class SchoolDates(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f'Starts: {self.start_date}, Ends: {self.end_date}'