from django.db import models
from django.contrib import auth

class User(auth.models.User, auth.models.PermissionsMixin):
    messages = models.ManyToManyField('messaging.Message', related_name='messages')

    def __str__(self):
        return self.username