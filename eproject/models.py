from django.db import models
from django.contrib.auth.models import User
from datetime import datetime,date

# Create your models here.
class team(models.Model):
    lead_name = models.CharField(max_length=30)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    enroll_no = models.CharField(max_length=30)
    email = models.CharField(max_length=30)
    contact_no = models.IntegerField()
    role = models.CharField(max_length=30)

    def __str__(self):
        return self.first_name


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.FileField(upload_to='profile_image', blank=True)

class ProjectUpload(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    desc = models.CharField(max_length=400)
    tech = models.CharField(max_length=50)
    v_link = models.CharField(max_length=200)
    project_file = models.FileField(upload_to='Projects', blank=False)
    p_report =  models.FileField(upload_to='Project_report', blank=False)
    upload_date = models.DateField(auto_now_add=True, blank=False)
    def __str__(self):
        return self.user.username

class Comment(models.Model):
    username = models.CharField(max_length=30,null=True)
    content = models.CharField(max_length=300)
    date = models.DateField(auto_now_add=True, blank=False)
    time = models.TimeField(auto_now=False, auto_now_add=True)