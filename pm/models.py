from django.db import models
from django.utils import timezone

# Create your models here.

REGION_CHIOCES = [
    ("NR", "North"),
    ("SR", "South"),
    ("ER", "East"),
    ("WR", "West"),
    ("CR", "Centeral"),
    ("NN", "None")
]


class Bank(models.Model):
    bank_name = models.CharField(max_length=50)
    bank_key = models.CharField(max_length=40)

    def __str__(self):
        return self.bank_name


class Region(models.Model):

    name = models.CharField(max_length=30)
    region = models.CharField(max_length=2, choices=REGION_CHIOCES)

    def __str__(self):
        return self.name


class BankBranch(models.Model):
    bank_name = models.ForeignKey(Bank, on_delete=models.PROTECT)
    region = models.CharField(max_length=2, choices=REGION_CHIOCES)
    district = models.CharField(max_length=30)
    branch_name = models.CharField(max_length=255)
    branch_key = models.CharField(max_length=50)
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

    def __str__(self) -> str:
        return self.terminal_name


class Schedule(models.Model):
    STATUS = [
        ("PE", "Pending"),
        ("OP", "Onprogress"),
        ("CO", "Completed"),
        ("CA", "Cancled")
    ]
    bank_name = models.ForeignKey(Bank, on_delete=models.CASCADE)
    terminal_name = models.ForeignKey(Terminal, on_delete=models.PROTECT)
    start_date = models.DateTimeField(
        auto_now_add=False, editable=True)
    end_date = models.DateTimeField(auto_now_add=False, editable=True)
    assign_to = models.ForeignKey(Engineer, on_delete=models.CASCADE)
    status = models.CharField(max_length=2, choices=STATUS, default=STATUS[0])
    description = models.CharField(max_length=300)

    def __str__(self) -> str:
        return str(self.terminal_name)
