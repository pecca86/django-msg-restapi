from django.db import models
from django.utils import timezone
# from accounts.models import User
from django.contrib import auth

# Create your models here.
class Message(models.Model):
    message_text = models.CharField(max_length=500)
    normalized_msg_text = models.CharField(max_length=500, default=None, blank=True, null=True)
    send_date = models.DateTimeField('date send', default=None)
    received_date = models.DateTimeField('date received', default=timezone.now, null=True)

    # sender = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='sender', default=None)
    # receiver_id = models.BigIntegerField(default=0)
    # sender_id = models.BigIntegerField(default=0)
    # receiver = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='receiver', default=None)
    receiver = models.ForeignKey(auth.models.User, on_delete=models.CASCADE, related_name='receiver', default=None)
    sender = models.ForeignKey(auth.models.User, on_delete=models.CASCADE, related_name='sender', default=None)


    is_read = models.BooleanField(default=False) # when user fetches messages / message by ID, set is_read to True 

    def __str__(self):
        return self.message_text

    def save(self, *args, **kwargs):
        self.normalized_msg_text = self.message_text.lower().strip()
        self.send_date = timezone.now()
        # self.sender = User.objects.get(pk=1)
        super(Message, self).save(*args, **kwargs)
        
    class Meta:
        verbose_name = "Message"
        verbose_name_plural = "Messages"
        ordering = ['send_date']


    


# from django.contrib import auth
# class User(auth.models.User, auth.models.PermissionsMixin):

#     def __str__(self):
#         return self.username
