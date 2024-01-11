from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

# Create your models here.



class student(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    avatar = models.ImageField(upload_to='images/avatar/', null=True, blank=True)
    document_file = models.FileField(upload_to='documents/',null=True, blank=True)
    description = RichTextField(blank=True, null=True)

    def __str__(self):
        return self.name
    


# class CustomUser(AbstractUser):
#     # Thêm các trường tùy chỉnh nếu cần
#     age = models.PositiveIntegerField(null=True, blank=True)
    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    test = models.CharField(null=True, blank=True, max_length=255)     


# class CustomUser(AbstractUser):
#     tesst1 = models.IntegerField(null=True, blank=True)

