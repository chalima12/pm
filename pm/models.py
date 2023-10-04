from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import CustomUserManager
# Create your models here.

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import CustomUserManager

# Create your models here.

REGION_CHIOCES = [
    ("NR", "North"),
    ("SR", "South"),
    ("ER", "East"),
    ("WR", "West"),
    ("CR", "Centeral"),
    ("NN", "None")
]


class User(AbstractBaseUser, PermissionsMixin):
    MALE = 'M'
    FEMALE = 'F'
    gender_choices = [
        (MALE, 'Male'),
        (FEMALE, 'Female'),
    ]
    # Basic information
    email = models.EmailField(("email address"), unique=True, null=True)
    username = models.CharField(unique=True, max_length=255, null=True)
    first_name = models.CharField(max_length=255, null=True)
    last_name = models.CharField(max_length=255, null=True)
    gender = models.CharField(
        max_length=100, choices=gender_choices, help_text="Gender", null=True, blank=True)
    phone = models.CharField(
        max_length=100, help_text='Phone Number', null=True, blank=True)
    Photo = models.ImageField(
        help_text='Photo', null=True, blank=True, default='atm_U2G9mVp.png')
    address = models.TextField(
        max_length=50, help_text='Address', null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    # Informtion for system access
    is_staff = models.BooleanField(default=False, null=True)
    is_active = models.BooleanField(default=True, null=True)
    is_moti = models.BooleanField(default=False, null=True)
    is_User = models.BooleanField(default=False, null=True)
    is_bank = models.BooleanField(default=False, null=True)
    system_summary = models.BooleanField(default=False, null=True, blank=True)
    equipment_usage = models.BooleanField(default=False, null=True, blank=True)
    view_user_list = models.BooleanField(default=False, null=True, blank=True)
    edit_user = models.BooleanField(default=False, null=True, blank=True)
    assign_privilege = models.BooleanField(
        default=False, null=True, blank=True)
    see_user_detail = models.BooleanField(default=False, null=True, blank=True)
    upload_daily_report = models.BooleanField(
        default=False, null=True, blank=True)
    view_contact_list = models.BooleanField(
        default=False, null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return str(self.first_name) + " " + str(self.last_name)


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
    assign_to = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=2, choices=STATUS, default=STATUS[0])
    description = models.CharField(max_length=300)

    def __str__(self) -> str:
        return str(self.terminal_name)
