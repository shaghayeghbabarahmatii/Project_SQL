from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    phonenumber = models.CharField(null=True, blank=True, max_length=11, verbose_name='شماره تلفن')
    cardnumber = models.CharField(null=True,blank=True,max_length=16,verbose_name='شماره کارت')
    idnumber = models.CharField(null=True,blank=True,max_length=10,verbose_name='شماره ملی')
    is_author = models.BooleanField(default=False, verbose_name="وضعیت مشاوره")
    is_supervisor = models.BooleanField(default=False, verbose_name="وضعیت سرپرست")