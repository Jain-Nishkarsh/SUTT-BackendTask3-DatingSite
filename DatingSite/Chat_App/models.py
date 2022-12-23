from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class messages(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    receiver  = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
    content = models.TextField(blank=True)
    read = models.BooleanField(default=False)
    timeSent = models.DateTimeField(default= timezone.now)