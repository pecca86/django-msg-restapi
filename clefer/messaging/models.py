from django.db import models
from django.utils import timezone
from django.contrib import auth

class Message(models.Model):
    message_text = models.CharField(max_length=500)
    normalized_msg_text = models.CharField(max_length=500, default=None, blank=True, null=True)
    send_date = models.DateTimeField('date send', default=None)
    received_date = models.DateTimeField('date received', default=timezone.now, null=True)
    receiver = models.ForeignKey(auth.models.User, on_delete=models.CASCADE, related_name='receiver', default=None)
    sender = models.ForeignKey(auth.models.User, on_delete=models.CASCADE, related_name='sender', default=None)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.message_text

    def save(self, *args, **kwargs):
        self.normalized_msg_text = self.message_text.lower().strip()
        self.send_date = timezone.now()
        super(Message, self).save(*args, **kwargs)
        
    class Meta:
        verbose_name = "Message"
        verbose_name_plural = "Messages"
        ordering = ['send_date']