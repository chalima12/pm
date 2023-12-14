from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import CustomUserManager
# Create your models here.

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
    MANAGER ="MA"
    SCHEDULER ="SC"
    ENGINEER ="EN"
    BANKER= "BA"
    user_type = [(MANAGER, "Manager"),
                (SCHEDULER, "Scheduler"),
                (ENGINEER, "Engineer"),
                (BANKER, "Bank User"),
                ]
    # Basic information
    email = models.EmailField(("email address"), unique=True, null=True)
    username = models.CharField(
        unique=True, max_length=255, null=True, blank=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    gender = models.CharField(
        max_length=100, choices=gender_choices, help_text="Gender", null=True, blank=True)
    phone = models.CharField(
        max_length=100, help_text='Phone Number', null=True, blank=True)
    Photo = models.ImageField(
        help_text='Photo', null=True, blank=True, default='atm_U2G9mVp.png')
    address = models.TextField(
        max_length=50, help_text='Address', null=True, blank=True)
    date_joined = models.DateTimeField(
        auto_now_add=True, null=True, blank=True)
    is_staff = models.BooleanField(default=True, null=True, blank=True)
    is_active = models.BooleanField(default=True, null=True, blank=True)
    is_superuser = models.BooleanField(default=False,null=True,blank=True)
    user_type = models.CharField(max_length=40,choices=user_type)

    # Permissions and Roles
    view_dashboard = models.BooleanField(default=False, null=True, blank=True)
    view_users = models.BooleanField(default=False, null=True, blank=True)
    view_banks = models.BooleanField(default=False, null=True, blank=True)
    view_terminals = models.BooleanField(default=False, null=True, blank=True)
    view_scheules = models.BooleanField(default=False, null=True, blank=True)
    view_report = models.BooleanField(default=False, null=True, blank=True)
    # edit Permissions
    edit_user = models.BooleanField(default=False, null=True, blank=True)
    edit_bank = models.BooleanField(default=False, null=True, blank=True)
    edit_terminal = models.BooleanField(default=False, null=True, blank=True)
    
    # Add Permissions
    add_user = models.BooleanField(default=False, null=True, blank=True)
    add_bank = models.BooleanField(default=False, null=True, blank=True)
    add_terminals = models.BooleanField(default=False, null=True, blank=True)

    # Funtional based Permissions
    make_schedule = models.BooleanField(default=False, null=True, blank=True)
    assign_engineer = models.BooleanField(default=False, null=True, blank=True)
    start_task = models.BooleanField(default=False, null=True, blank=True)
    re_assign_engineer = models.BooleanField(default=False, null=True, blank=True)
    end_task = models.BooleanField(default=False, null=True, blank=True)
    approve_task = models.BooleanField(default=False, null=True, blank=True)
    reject_task = models.BooleanField(default=False, null=True, blank=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return str(self.first_name) + " " + str(self.last_name)
    class Meta:
        ordering = ['first_name', 'last_name']


class Bank(models.Model):
    bank_name = models.CharField(max_length=50, null=True, blank=True)
    bank_key = models.CharField(max_length=40, null=True, blank=True)
    is_active = models.BooleanField(default=True, null=True, blank=True)
    created_date = models.DateField(
        auto_now_add=True)


    def __str__(self):
        return self.bank_name
    class Meta:
        ordering = ['bank_name']

class Terminal(models.Model):
    NORTH = "NR"
    SOUTH = "SR"
    EAST = "ER"
    WEST = "WR"
    CENTERAL = "CR"
    MOTI_DISTRICT = [
        (NORTH, "North"),
        (SOUTH, "South"),
        (EAST, "East"),
        (WEST, "West"),
        (CENTERAL, "Centeral"),
    ]

    bank_name = models.ForeignKey(
        Bank, on_delete=models.PROTECT,null=True,blank=True,related_name='terminalBanks')
    bank_district = models.CharField(max_length=255, null=True, blank=True)
    bank_branch = models.CharField(max_length=255,null=True,blank=True)
    moti_district = models.CharField(
        max_length=50, choices=MOTI_DISTRICT, null=True, blank=True)
    tid = models.CharField(max_length=30, null=True, blank=True)
    terminal_name = models.CharField(max_length=255, null=True, blank=True)
    serial_number = models.CharField(max_length=200, null=True, blank=True)
    model = models.CharField(max_length=200, null=True, blank=True)
    disspenser_type = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    location = models.CharField(max_length=255,null=True,blank=True)
    created_date = models.DateField(
        auto_now_add=True)
    

    def __str__(self) -> str:
        return self.terminal_name
    
    class Meta:
        ordering = ['terminal_name']

class AllSchedule(models.Model):
    schedul_name = models.CharField(max_length=1000, null=True, blank=True)
    scheduled_by = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)
    description = models.CharField(max_length=300, null=True, blank=True)
    def __str__(self):
        return self.schedul_name
    

class Schedule(models.Model): #TODO: name this to Shedule List
    PENDING = 'PE'
    WAITING = "WT"
    ONPROGRESS = 'OP'
    APPROVED ='AP'
    REJECTED='RE'
    SUBMITTED = 'SB'
    APPROVED ="AP"
    status_choices = [
        (PENDING, 'Pending'),
        (WAITING,'Waiting'),
        (ONPROGRESS, 'Onprogress'),
        (SUBMITTED, 'Sumitted'),
        (APPROVED, 'Approved'),
        (REJECTED, 'Rejected'),

    ]
    HIGH = 'H'
    MEDIUM = 'M'
    LOW = 'L'
    priority_choice = [
        (HIGH, 'High'), 
        (MEDIUM, 'Medium'), 
        (LOW, 'Low')
        ]
    schedule = models.ForeignKey(AllSchedule, models.PROTECT, related_name='all_schedules',null=True, blank=True)
    terminal = models.ForeignKey(
        Terminal, on_delete=models.PROTECT, help_text='Select Terminal', related_name='terminals', null=True)
    start_date = models.DateTimeField(
        auto_now_add=False, editable=True, null=True, blank=True)
    end_date = models.DateTimeField(
        auto_now_add=False, editable=True,null=True,blank=True)
    assign_to = models.ForeignKey(
        User, on_delete=models.PROTECT,null=True, blank=True)
    status = models.CharField(
        max_length=10, choices=status_choices, default=PENDING,null=True,blank=True)
    terminal = models.ForeignKey(
        Terminal, on_delete=models.PROTECT, help_text='Select Terminal', null=True)
    priority = models.CharField(
        max_length=10, choices=priority_choice,null=True,blank=True)
    material_required = models.CharField(max_length=255, null=True,blank=True)
    comment = models.CharField(max_length=255,null=True,blank=True)
    checklist_photo = models.FileField(null=True, blank=True,upload_to="pm_checklist_pics/")
    closed_date = models.DateTimeField(blank=True,null=True,default=timezone.now)
    approval_comment = models.CharField(max_length=100, null=True, blank=True)
    
    created_date = models.DateField(
        auto_now_add=True)
    

    def __str__(self) -> str:
        return str(self.terminal)
    
    # def remaining_days(self):
    #     today = timezone.now().date()
    #     days_elapsed = (today - self.start_date).days
    #     remaining_days = max(0, 90 - days_elapsed)
    #     return remaining_days
    class Meta:
        ordering = ['end_date']
        
    


