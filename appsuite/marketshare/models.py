
from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class MarketShare(models.Model):
    owner=models.ForeignKey(User)
    symbol=models.CharField(max_length=100)
    account=models.CharField(max_length=500)
    createTime=models.datetime.datetime.now()

from django.forms import ModelForm

class MsForm(ModelForm):
    class Meta:
        model=MarketShare
        exclude = ['owner']
