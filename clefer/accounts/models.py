from django.db import models
# from django.contrib.auth.models import User
from django.contrib import auth




# Create your models here.
# class User(models.Model):
#     username = models.CharField(max_length=50)
#     email = models.EmailField()
#     password = models.CharField(max_length=50)
#     messages = models.ManyToManyField('messaging.Message', related_name='messages')
    
#     def __str__(self) -> str:
#         return self.username

class User(auth.models.User, auth.models.PermissionsMixin):
    messages = models.ManyToManyField('messaging.Message', related_name='messages', blank=True, null=True)

    def __str__(self):
        return self.username