from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class ReportUser(models.Model):
    reporter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reporter')
    reportee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reportee')
    reportTime = models.DateTimeField(default=timezone.now)
    reportMessage = models.TextField(blank=True, max_length=100)
