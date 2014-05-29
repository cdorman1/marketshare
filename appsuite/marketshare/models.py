from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class GetSymbol(models.Model):
    owner=models.ForeignKey(User)
    symbol=models.CharField(max_length=100)
    account=models.CharField(max_length=500)
    createTime=models.DateTimeField()
