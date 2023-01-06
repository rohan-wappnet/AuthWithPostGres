from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class details(models.Model):
    id = models.AutoField(primary_key=True)
    user = user = models.ForeignKey(
        User, null=False, on_delete=models.CASCADE, blank=False
    )
    city = models.CharField(max_length=30)
    phone = models.BigIntegerField()