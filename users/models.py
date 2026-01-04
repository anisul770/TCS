from django.db import models
from django.contrib.auth.models import AbstractUser
from users.managers import CustomUserManager

# Create your models here.
class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True,null=True)
    phone_number = models.CharField(max_length=15,blank=True,null=True)
    facebook_link = models.URLField(blank=True,null=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    objects = CustomUserManager()
    
    def __str__(self):
        return self.email
    
class ProfileImage(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='profile_pic')
    profile_pic = models.ImageField(upload_to='user/profile')