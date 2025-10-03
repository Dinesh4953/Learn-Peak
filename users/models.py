from django.db import models

# Create your models here.
# models.py
from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True)
    codeforces_handle = models.CharField(max_length=100, blank=True, null=True)  

    # cv fields
    name_cv = models.CharField(max_length=1000, blank=True)
    email_cv = models.EmailField(max_length=300, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    summary = models.TextField(blank=True)
    degree = models.CharField(max_length=200, blank=True)
    school = models.CharField(max_length=200, blank=True)
    university = models.CharField(max_length=200, blank=True)
    previous_work = models.TextField(blank=True)
    skills = models.TextField(blank=True)


    def __str__(self):
        return self.user.username
