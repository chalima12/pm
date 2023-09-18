from django.db import models

# Create your models here.
class Bank(models.Model):
    bank_name =models.CharField(max_length=50)
    bank_key = models.CharField(max_length=40)
