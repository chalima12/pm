from django.db import models

# Create your models here.
class Bank(models.Model):
    bank_name =models.CharField(max_length=50)
    bank_key = models.CharField(max_length=40)

    def __str__(self):
            return self.bank_name
        

class Region(models.Model):
   REGION_CHIOCES = [
    ("NR", "North"),
    ("SR", "South"),
    ("ER", "East"),
    ("WR", "West"),
    ("CR", "Centeral"),
    ("NN","None")
]
   name = models.CharField(max_length=30)
   region = models.CharField(max_length=2,choices=REGION_CHIOCES)
   def __str__(self):
       return self.name
   
class BankBranch(models.Model):
    bank_name = models.ForeignKey(Bank, on_delete=models.CASCADE)

    def __str__(self):
        return self.bank_name

class Engineer(models.Model):
    GENDER =[("M","Male"),("F","Female")]
    firstName = models.CharField(max_length=100 ,null=False)
    lastName = models.CharField(max_length=100,null=False)
    phoneNumber = models.IntegerField()
    gender = models.CharField(max_length=1, choices=GENDER)
    
    def __str__(self):
        return self.firstName
    