from django.db import models
from django.utils import timezone

# Create your models here.


class Bank(models.Model):
    bank_name = models.CharField(max_length=50)
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
        ("NN", "None")
    ]
    name = models.CharField(max_length=30)
    region = models.CharField(max_length=2, choices=REGION_CHIOCES)

    def __str__(self):
        return self.name


class BankBranch(models.Model):
    baranch_name = models.ForeignKey(Bank, on_delete=models.PROTECT)
    location = models.CharField(max_length=255)

    def __str__(self):
        return self.baranch_name


class Engineer(models.Model):
    GENDER = [("M", "Male"), ("F", "Female")]
    firstName = models.CharField(max_length=100, null=False)
    lastName = models.CharField(max_length=100, null=False)
    gender = models.CharField(max_length=1, choices=GENDER)
    phoneNumber = models.IntegerField()
    email = models.EmailField(max_length=255)

    def __str__(self):
        return self.firstName + self.lastName


class Terminal(models.Model):
    MOTI_DISTRICT = [
        ("NR", "North"),
        ("SR", "South"),
        ("ER", "East"),
        ("WR", "West"),
        ("CR", "Centeral"),
        ("NN", "None")
    ]

    bank_name = models.ForeignKey(Bank, on_delete=models.PROTECT)
    bank_district = models.CharField(max_length=255, null=True)
    bank_branch = models.CharField(max_length=255)
    moti_district = models.CharField(max_length=50, choices=MOTI_DISTRICT)
    tid = models.CharField(max_length=30)
    terminal_name = models.CharField(max_length=255)
    serial_number = models.CharField(max_length=200)
    model = models.CharField(max_length=200, null=True)
    disspenser_type = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    location = models.CharField(max_length=255)


class Schedule(models.Model):
    STATUS = [
        ("0", "Pending"),
        ("1", "Onprogress"),
        ("3", "Completed"),
        ("4", "Cancled")
    ]
    terminal_name = models.ForeignKey(Terminal, on_delete=models.PROTECT)
    starting_date = models.DateTimeField(auto_now_add=True,)
    end_date = models.DateTimeField()
    status = models.CharField(max_length=2, choices=STATUS)
    description = models.CharField(max_length=300)
