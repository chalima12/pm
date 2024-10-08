from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib import messages
from django.http import Http404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime, timezone, timedelta, date
from django.db.models import Count
from django.utils import timezone
import json
from pm.models import Terminal, User, Bank, Schedule, AllSchedule,Moti_district
import math
from pm.forms import *

NORTH = "North"
SOUTH = "South"
EAST = "East"
WEST = "West"
CENTRAL = "Central"
MOTI_DISTRICT = [
        (NORTH, "North"),
        (SOUTH, "South"),
        (EAST, "East"),
        (WEST, "West"),
        (CENTRAL, "Central"),
    ]


def calculate_schedule_statistics(schedules):
    specific_schedule_count = schedules.count()
    pending_schedule = schedules.filter(status="PE").count()
    waiting_schedule = schedules.filter(status="WT").count()
    onprogress_schedule = schedules.filter(status="OP").count()
    submitted_schedule = schedules.filter(status="SB").count()
    approved_schedule = schedules.filter(status="AP").count()
    rejected_schedule = schedules.filter(status="RE").count()

    if specific_schedule_count > 0:
        pending_rate = round(pending_schedule / specific_schedule_count * 100, 2)
        waiting_rate = round(waiting_schedule / specific_schedule_count * 100, 2)
        onprogress_rate = round(onprogress_schedule / specific_schedule_count * 100, 2)
        submitted_rate = round(submitted_schedule / specific_schedule_count * 100, 2)
        approved_rate = round(approved_schedule / specific_schedule_count * 100, 2)
        rejected_rate = round(rejected_schedule / specific_schedule_count * 100, 2)
    else:
        pending_rate = 0
        waiting_rate = 0
        onprogress_rate = 0
        submitted_rate = 0
        approved_rate = 0
        rejected_rate = 0

    tasks = pending_schedule + waiting_schedule + onprogress_schedule + rejected_schedule
    days_needed = round(tasks / 7, 2)

    return {
        "specific_schedule_count": specific_schedule_count,
        "pending_schedule": pending_schedule,
        "waiting_schedule": waiting_schedule,
        "onprogress_schedule": onprogress_schedule,
        "submitted_schedule": submitted_schedule,
        "approved_schedule": approved_schedule,
        "rejected_schedule": rejected_schedule,
        "pending_rate": pending_rate,
        "waiting_rate": waiting_rate,
        "onprogress_rate": onprogress_rate,
        "submitted_rate": submitted_rate,
        "approved_rate": approved_rate,
        "rejected_rate": rejected_rate,
        "days_needed": days_needed,
    }


def login_user(request):
    resp = {"status": 'failed', 'msg': ''}
    username = ''
    password = ''
    if request.POST:
        username = request.POST['email']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                resp['status'] = 'success'
            else:
                resp['msg'] = "Incorrect username or password"
        else:
            resp['msg'] = "Incorrect username or password"
    return HttpResponse(json.dumps(resp), content_type='application/json')

# Logout


def logoutuser(request):
    logout(request)
    return redirect('/')


@login_required
def home(request):
    if request.user.is_authenticated:
        loggedin_user_type = request.user.user_type
        # print(loggedin_user_type)
        logged_in_user = request.user
    else:
        loggedin_user_type = None
        logged_in_user = None
    numOfBanks = Bank.objects.all().count()
    numOfUsers = User.objects.all().count()
    numberofTerminals = Terminal.objects.all().count()
    pendingTerminals = Schedule.objects.filter(status="PE").count()
    pendingLists = Schedule.objects.filter(status="PE").all()
    pendingSchedule = Schedule.objects.filter(status="PE").count()
    waitingSchedule = Schedule.objects.filter(status="WT").count()
    onprogressSchedule = Schedule.objects.filter(status="OP").count()
    submittedSchedule = Schedule.objects.filter(status="SB").count()
    approvedSchedule = Schedule.objects.filter(status="AP").count()
    rejectedSchedule = Schedule.objects.filter(status="RE").count()
    high_priority_schedules = Schedule.objects.filter(priority="H")

    allSchedule = pendingSchedule + waitingSchedule + onprogressSchedule + \
        submittedSchedule + approvedSchedule + rejectedSchedule
    context = {
        "company": "Moti Engineering PLC",
        "projectName": "Preventive Maintainace For ATMS",
        'title': "Dashboard",
        'numOfBanks': numOfBanks,
        'numOfUsers': numOfUsers,
        'numberofTerminals': numberofTerminals,
        "pendingTerminals": pendingTerminals,
        "pendingLists": pendingLists,
        'allSchedule': allSchedule,
        "logged_in_user": logged_in_user,
        "user_type": loggedin_user_type,
        "schedules": high_priority_schedules,

    }
    return render(request, "pm/overviewDashboard.html", context)

@login_required
def user(request):
    UsersQuerySet = User.objects.all()
    context = {
        "title": "All Users",
        "users": UsersQuerySet
    }
    return render(request, 'pm/engineers.html', context)
   

@login_required
def user_card_display(request):
    UsersQuerySet = User.objects.all()
    context = {
        "title": "All Users",
        "users": UsersQuerySet
    }
    return render(request, 'pm/user_card_display.html', context)

def view_user(request, id):
    return HttpResponseRedirect(reverse('all-engineers'))


def add_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "New User created successfully!")
            return redirect('all-engineers')
    else:
        form = UserForm()
    context = {'form': form, "title": "Add User"}
    return render(request, 'pm/add_user.html', context)

@login_required
def edit_user(request, user_id):
    user = User.objects.get(pk=user_id)
    user_form = UserEditForm(request.POST or None,request.FILES or None, instance=user)

    if request.method == 'POST':
        if user_form.is_valid():
            user_form.save()
            messages.success(request, "User information updated successfully!")
            return redirect('all-engineers')
        else:
            messages.error(request, "Please correct the errors in the form.")

    context = {
        'user': user,
        'form': user_form,
        "title": "Edit User"
    }
    return render(request, 'pm/update_user.html', context)

@login_required
def change_password(request):
    password_form = UserPasswordChangeForm(
        request.user, request.POST or None)
    if request.method == 'POST':
        if password_form.is_valid():
            password_form.save()
            update_session_auth_hash(request, request.user)
            messages.success(request, "Password changed successfully!")
            return redirect('all-engineers')
        else:
            messages.error(request, "Please correct the errors in the form.")
    context = {
        'form': password_form,
        "title": "Change Password"
    }
    return render(request, 'pm/password_change.html', context)

@login_required
def userProfile(request):
    return render(request, 'pm/profile.html')


def assign_permissions(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = AssignPermissionsForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            # Redirect to the desired URL after successful update
            return redirect('all-engineers')
    else:
        form = AssignPermissionsForm(instance=user)
    context = {'form': form, "title": "Add Permissions", "user": user}
    return render(request, 'pm/assign_permissions.html', context)

@login_required
def add_moti_district(request):
    if request.method == "POST":
        form = MotiDistrictForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Moti District Add Successfully")
            return redirect('districts-list')
    else:
        form = MotiDistrictForm()
    context ={"form":form,"title":"Add Moti District"}
    return render(request,"pm/add_district.html",context)
from django.shortcuts import get_object_or_404

@login_required
def update_moti_district(request, district_id):
    district = get_object_or_404(Moti_district, id=district_id)
    if request.method == "POST":
        form = MotiDistrictForm(request.POST, instance=district)
        if form.is_valid():
            form.save()
            messages.success(request, "Moti District Updated Successfully")
            return redirect('districts-list')
    else:
        form = MotiDistrictForm(instance=district)

    context = {"form": form, "title": "Edit Moti District"}
    return render(request, "pm/update_district.html", context)

@login_required
def moti_districts(request):
        districts = Moti_district.objects.all()
        context = {
            "title": "Moti Districts",
            "districts": districts
        }
        return render(request, 'pm/moti_districts.html', context)
@login_required
def banks(request):
    try:
        banksQuerySet = Bank.objects.all()
        context = {
            "title": "List of All Banks",
            "banks": banksQuerySet
        }
        return render(request, 'pm/banks.html', context)
    except:
        raise Http404()


    
@login_required
def addBank(request):
    success = False
    if request.method == "POST":
        form = BankForm(request.POST)
        if form.is_valid():
            form.save()
            success = True
            messages.success(request, "New Bank Add Successfully!")
            return redirect('banks-page')
    else:
        form = BankForm()
    context = {"form": form, "title": "Add Bank", "success": success}
    return render(request, 'pm/addBank.html', context)


@login_required
def updateBank(request, bank_id):
    bank = Bank.objects.get(pk=bank_id)
    form = BankForm(request.POST or None, instance=bank)
    success = False
    if form.is_valid():
        form.save()
        success = True
        messages.info(request, "Updated Successfully!")
        return redirect('banks-page')
    context = {
        'bank': bank,
        'form': form,
        "title": "Edit Bank",
        "success": success
    }
    return render(request, 'pm/update_bank.html', context)


@login_required
def deactivate_bank(request, bank_id):
    bank = Bank.objects.get(pk=bank_id)
    bank.is_active = False
    bank.save()
    return HttpResponseRedirect(reverse('banks-page'))


@login_required
def activate_bank(request, bank_id):
    bank = Bank.objects.get(pk=bank_id)
    bank.is_active = True
    bank.save()
    return HttpResponseRedirect(reverse('banks-page'))


@login_required
def terminals(request):
    terminalsQuerySet = Terminal.objects.all()
    context = {
        "title": "Terminals",
        "terminals": terminalsQuerySet,
    }
    return render(request, 'pm/terminals.html', context)


@login_required
def view_terminal(request, id):
    return HttpResponseRedirect(reverse('all-terminals'))


@login_required
def addTerminal(request):
    if request.method == "POST":
        form = TerminalForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "New Terminals Add Successfully!")
            return redirect('all-terminals')
    else:
        form = TerminalForm()
    context = {"form": form, "title": "Add Terminal"}
    return render(request, 'pm/addTerminal.html', context)


@login_required
def updateTerminal(request, terminal_id):
    terminal = Terminal.objects.get(pk=terminal_id)
    form = TerminalForm(request.POST or None, instance=terminal)
    if form.is_valid():
        form.save()
        return redirect('all-terminals')
    context = {
        'bank': terminal,
        'form': form,
        "title": "Edit Terminal"
    }
    return render(request, 'pm/update_terminal.html', context)


@login_required
def all_schedule(request):
    all_schedule = AllSchedule.objects.all()
    context = {
        "title": "Scheduled ATMS",
        "schedules": all_schedule,
    }
    return render(request, 'pm/schedule.html', context)

@login_required
def detail_schedules_list(request, pk):
    schedule = get_object_or_404(AllSchedule, pk=pk)
    schedules_list = Schedule.objects.filter(schedule=schedule)
    specific_schedule_statistics = calculate_schedule_statistics(schedules_list)
    
    # now = datetime.now(timezone.utc)
    # for schedule in schedules_list:
    #     schedule.remaining_days = (schedule.end_date - now).days

    context = {
        'schedules': schedules_list,
        "title": "Detail Schedule",
        **specific_schedule_statistics,
    }
    return render(request, 'pm/detail_schedules_list.html', context)


@login_required
def user_specific_tasks(request):
    user_id = request.user.id
    schedules_list = Schedule.objects.filter(assign_to=user_id)

    # Calculate schedule statistics
    schedule_statistics = calculate_schedule_statistics(schedules_list)

    # Calculate remaining days for each schedule
    now = datetime.now(timezone.utc)
    for schedule in schedules_list:
        schedule.remaining_days = (schedule.end_date - now).days

    context = {
        'schedules': schedules_list,
        "title": "Detail schedule",
        **schedule_statistics,
    }
    return render(request, 'pm/user_tasks.html', context)

@login_required
def create_schedule(request):
    tqs = Terminal.objects.all()
    if request.method == 'POST':
        form = ScheduleForm(request.POST)
        form1 = AllScheduleForm(request.POST)
        if form.is_valid() and form1.is_valid():
            form1_instance = form1.save(commit=False)
            form1_instance.scheduled_by = request.user
            form1_instance.save()
            terminals = form.cleaned_data['terminals']
            start_date = form.cleaned_data['start_date']
            string_start_date = str(date.isoformat(start_date))
            formated_start_date = datetime.strptime(
                string_start_date, "%Y-%m-%d")
            end_date = formated_start_date + timedelta(days=90)
            for terminal in terminals:
                Schedule.objects.create(
                    schedule=form1_instance,
                    terminal=terminal,
                    start_date=start_date,
                    end_date=end_date,
                )

            messages.success(request, "Schedules created successfully!")
            return redirect('schedules')
    else:
        form = ScheduleForm()
        form1 = AllScheduleForm()
    return render(request, 'pm/addSchedule.html', {'form': form, "terminals": tqs, "form1": form1})


@login_required
def assign_engineer(request, id):
    if request.method == 'POST':
        schedule = Schedule.objects.get(pk=id)
        all_schedule_id = schedule.schedule.id
        form = AssignEngineerForm(request.POST, instance=schedule)
        if form.is_valid():
            schedule.status = "WT"
            form.save()
            messages.success(request, "Engineer Assigned successfully!")
            return redirect(f'/detail_schedule/{all_schedule_id}')

    else:
        schedule = Schedule.objects.get(pk=id)
        all_schedule_id = schedule.schedule.id
        form = AssignEngineerForm(instance=schedule)
    context = {'form': form,
               'schedule': schedule,
               "title": "Assign Engineer",
               'all_schedule_id': all_schedule_id

               }
    return render(request, 'pm/assign_engineer.html', context)


def start_task(request, scheule_id):
    schedule = Schedule.objects.get(pk=scheule_id)
    all_schedule_id = schedule.schedule.id
    schedule.status = "OP"
    schedule.save()
    return redirect(f'/detail_schedule/{all_schedule_id}')


@login_required
def end_scheduled_task(request, id):
    if request.method == 'POST':
        schedule = Schedule.objects.get(pk=id)
        all_schedule_id = schedule.schedule.id
        form = EndScheduleForm(request.POST, request.FILES, instance=schedule)
        if form.is_valid():
            schedule.status = "SB"
            form.save()
            messages.success(request, "Change Updated successfully!")
            return redirect(f'/detail_schedule/{all_schedule_id}')
    else:
        schedule = Schedule.objects.get(pk=id)
        all_schedule_id = schedule.schedule.id
        form = EndScheduleForm(instance=schedule)
    context = {'form': form, 'schedule': schedule,
               "title": "End task", "all_schedule_id": all_schedule_id}
    return render(request, 'pm/end_schedule.html', context)


@login_required
def approve_task(request, id):
    if request.method == 'POST':
        schedule = Schedule.objects.get(pk=id)
        all_schedule_id = schedule.schedule.id
        form = ApprovalScheduleForm(
            request.POST, request.FILES, instance=schedule)
        if form.is_valid():
            schedule.status = "AP"
            form.save()
            messages.success(request, "Chenge Updated successfully!")
            return redirect(f'/detail_schedule/{all_schedule_id}')
    else:
        schedule = Schedule.objects.get(pk=id)
        form = ApprovalScheduleForm(instance=schedule)
        all_schedule_id = schedule.schedule.id
    context = {'form': form, 'schedule': schedule,
            "title": "Approval task", "all_schedule_id": all_schedule_id}
    return render(request, 'pm/task_approval.html', context)


def reject_task(request, id):
    if request.method == 'POST':
        schedule = Schedule.objects.get(pk=id)
        all_schedule_id = schedule.schedule.id

        form = ApprovalScheduleForm(
            request.POST, request.FILES, instance=schedule)
        if form.is_valid():
            schedule.status = "RE"
            form.save()
            messages.success(request, "Change Updated successfully!")
            return redirect(f'/detail_schedule/{all_schedule_id}')
    else:
        schedule = Schedule.objects.get(pk=id)
        form = ApprovalScheduleForm(instance=schedule)
        all_schedule_id = schedule.schedule.id
    context = {'form': form, 'schedule': schedule,
            "title": "Reject task", "all_schedule_id": all_schedule_id}
    return render(request, 'pm/task_approval.html', context)


#Scheduler 
def update_schedule_statuses():
    # Define quarters
    current_date = timezone.now().date()
    quarters = {
        1: (timezone.datetime(current_date.year - 1, 7, 1), timezone.datetime(current_date.year - 1, 9, 30)),
        2: (timezone.datetime(current_date.year - 1, 10, 1), timezone.datetime(current_date.year - 1, 12, 31)),
        3: (timezone.datetime(current_date.year, 1, 1), timezone.datetime(current_date.year, 3, 31)),
        4: (timezone.datetime(current_date.year, 4, 1), timezone.datetime(current_date.year, 6, 30)),
    }
    
    # Update schedules status for each quarter
    for quarter, (start_date, end_date) in quarters.items():
        # Get schedules ending within the current quarter
        schedules = Schedule.objects.filter(end_date__gte=start_date, end_date__lte=end_date)
        # Update status to "Pending" for each schedule
        schedules.update(status=Schedule.PENDING)


# Reports View


@login_required
def engineers_list(request):
    users = None
    title = "Users Report"
    selected = request.POST.get('options')
    from_date = request.POST.get('from_date')
    to_date = request.POST.get('to_date')
    if (selected == 'All users'):
        users = User.objects.filter(date_joined__range=(from_date, to_date))
        title = "All Users"
    if (selected == 'Engineers'):
        users = User.objects.filter(
            user_type="EN", date_joined__range=(from_date, to_date))
        title = "Engineers"
    if (selected == 'Active Users'):
        users = User.objects.filter(
            is_active=True, date_joined__range=(from_date, to_date))
        title = "Active Users"
    if (selected == 'InActive Users'):
        users = User.objects.filter(
            is_active=False, date_joined__range=(from_date, to_date))
        title = "InActive Users"
    if (selected == 'Super Users'):
        users = User.objects.filter(
            is_superuser=True, date_joined__range=(from_date, to_date))
        title = "Super Users"
    if (selected == 'Bank Users'):
        users = User.objects.filter(
            user_type = "BA", created_date__range=(from_date, to_date))
        title = "Bank Users"
    context = {
        "users": users,
        "title": title,
        'selected': selected

    }
    return render(request, 'pm/engineers_report.html', context)

@login_required
def banks_list(request):
    banks = Bank.objects.all()
    title = "Banks Report"
  
    context = {
        "banks": banks,
        "title": title,
    }
    return render(request, 'pm/banks_report.html', context)
@login_required
def districts_list(request):
    districts = Moti_district.objects.all()
    title = "Districts Report"

    context = {
        "districts": districts,
        "title": title,
    }
    return render(request, 'pm/districts_report.html', context)

@login_required
def schedule_report_by_district(request, district_id):
    schedules = Schedule.objects.filter(terminal__district__id=district_id)
    district = get_object_or_404(Moti_district, pk=district_id)
    specific_schedule_statistics_by_district = calculate_schedule_statistics(schedules)
    labels = ["Pending", "Waiting", "On Progress", "Submitted", "Approved", "Rejected"]
    dataset_data = [
        specific_schedule_statistics_by_district["pending_rate"],
        specific_schedule_statistics_by_district["waiting_rate"],
        specific_schedule_statistics_by_district["onprogress_rate"],
        specific_schedule_statistics_by_district["submitted_rate"],
        specific_schedule_statistics_by_district["approved_rate"],
        specific_schedule_statistics_by_district["rejected_rate"]
    ]

    context = {
        'schedules': schedules,
        'title': "Schedules by Moti district",
        "district": district,
        **specific_schedule_statistics_by_district,
        "labels": labels,
        "dataset_data": dataset_data,
    }

    return render(request, 'pm/schedules_by_district.html', context)



@login_required
def schedules_report_by_bank(request, bank_id):
    bank = get_object_or_404(Bank, pk=bank_id)
    title = "Schedules List"
    # schedule_list_by_bank = Schedule.objects.filter(terminal__bank_name = bank)
    terminals_in_bank = Terminal.objects.filter(bank_name=bank)
    # Filter schedules associated with the terminals in the bank
    schedule_list_by_bank = Schedule.objects.filter(
        terminal__in=terminals_in_bank)
    bank_schedule_statistics = calculate_schedule_statistics(schedule_list_by_bank)
    # Construct labels and dataset_data
    labels = ["Pending", "Waiting", "On Progress", "Submitted", "Approved", "Rejected"]
    dataset_data = [
        bank_schedule_statistics["pending_rate"],
        bank_schedule_statistics["waiting_rate"],
        bank_schedule_statistics["onprogress_rate"],
        bank_schedule_statistics["submitted_rate"],
        bank_schedule_statistics["approved_rate"],
        bank_schedule_statistics["rejected_rate"]
    ]
    context = {
        "schedules": schedule_list_by_bank,
        "title": title,
        "bank": bank,
        **bank_schedule_statistics,
        "labels": labels,
        "dataset_data": dataset_data
    }
    return render(request, 'pm/schedules_by_bank.html', context)






@login_required
def terminals_list(request):
    terminals = None
    title = "Terminals Report"
    selected = request.POST.get('options')
    from_date = request.POST.get('from_date')
    to_date = request.POST.get('to_date')
    if selected == "All Terminals":
        terminals = Terminal.objects.filter(
            created_date__range=(from_date, to_date))
        title = "All Terminals"
    else:
        # Get the region code based on the selected option
        region_code = None
        for code, region in MOTI_DISTRICT:
            if selected == f"{region} Terminals":
                region_code = code
                break
        if region_code is not None:
            # Filter terminals by the region code and date range
            terminals = Terminal.objects.filter(
                district__region=region_code,
                created_date__range=(from_date, to_date)
            )
            title = f"{selected}"

    context = {
        "terminals": terminals,
        "title": title,
        "selected": selected
    }
    return render(request, 'pm/terminals_report.html', context)

from django.utils import timezone
from django.db.models import Count, Q
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def private_banks_dashboard(request):
    # 1. Get List of Banks
    banks = Bank.objects.all()

    # 2. Count all schedules and approved schedules for each bank
    bank_schedule_counts = {}
    bank_approved_counts = {}

    for bank in banks:
        total_schedules = Schedule.objects.filter(terminal__bank_name=bank).count()
        approved_count = Schedule.objects.filter(terminal__bank_name=bank, status=Schedule.APPROVED).count()
        bank_schedule_counts[bank.bank_name] = total_schedules
        bank_approved_counts[bank.bank_name] = approved_count

    # 3. Calculate the percentage of approved schedules for each bank
    bank_approval_percentages = {}
    for bank in banks:
        total_approved = bank_approved_counts.get(bank.bank_name, 0)
        total_schedules = bank_schedule_counts.get(bank.bank_name, 0)
        if total_schedules > 0:
            approval_percentage = round((total_approved / total_schedules) * 100, 2)
        else:
            approval_percentage = 0
        bank_approval_percentages[bank.bank_name] = approval_percentage

    # 4. Define start and end dates for each quarter
    current_date = timezone.now().date()
    quarters = {
        'Q1': (timezone.make_aware(timezone.datetime(current_date.year - 1, 7, 1)), 
               timezone.make_aware(timezone.datetime(current_date.year - 1, 9, 30))),
        'Q2': (timezone.make_aware(timezone.datetime(current_date.year - 1, 10, 1)), 
               timezone.make_aware(timezone.datetime(current_date.year - 1, 12, 31))),
        'Q3': (timezone.make_aware(timezone.datetime(current_date.year, 1, 1)), 
               timezone.make_aware(timezone.datetime(current_date.year, 3, 31))),
        'Q4': (timezone.make_aware(timezone.datetime(current_date.year, 4, 1)), 
               timezone.make_aware(timezone.datetime(current_date.year, 6, 30))),
    }

    # 5. Initialize a dictionary to store data for each quarter
    quarter_data = {}

    # 6. Iterate over quarters and retrieve data for each quarter
    for quarter, (start_date, end_date) in quarters.items():
        # Filter schedules for the current quarter
        quarter_schedules = Schedule.objects.filter(start_date__gte=start_date, start_date__lte=end_date)

        # Count all schedules and approved schedules for each bank in the current quarter
        quarter_bank_schedule_counts = {}
        quarter_bank_approved_counts = {}

        for bank in banks:
            total_schedules = quarter_schedules.filter(terminal__bank_name=bank).count()
            approved_count = quarter_schedules.filter(terminal__bank_name=bank, status=Schedule.APPROVED).count()
            quarter_bank_schedule_counts[bank.bank_name] = total_schedules
            quarter_bank_approved_counts[bank.bank_name] = approved_count

        # Calculate the percentage of approved schedules for each bank in the current quarter
        quarter_bank_approval_percentages = {}
        for bank in banks:
            total_approved = quarter_bank_approved_counts.get(bank.bank_name, 0)
            total_schedules = quarter_bank_schedule_counts.get(bank.bank_name, 0)
            if total_schedules > 0:
                approval_percentage = round((total_approved / total_schedules) * 100, 2)
            else:
                approval_percentage = 0
            quarter_bank_approval_percentages[bank.bank_name] = approval_percentage

        # Store data for the current quarter
        quarter_data[quarter] = {
            "banks": banks,
            "bank_approval_percentages": quarter_bank_approval_percentages,
        }

    # 7. Create a context to pass the data to the template
    context = {
        "title": "Private Banks Dashboard",
        "bank_approval_percentages": bank_approval_percentages,
        "quarter_data": quarter_data,
    }
    print(quarter_data)

    return render(request, 'pm/private_banks_dashboard.html', context)

@login_required
def cbe_dashboard(request):
    # Get the list of districts
    districts = Moti_district.objects.all()
    # Get the current date in the current time zone
    current_date = timezone.now().date()
    # Define start and end dates for each quarter
    quarters = {
        1: (timezone.datetime(current_date.year -1, 7, 1), timezone.datetime(current_date.year -1, 9, 30)),  # Q1: July - September pervious year
        2: (timezone.datetime(current_date.year -1, 10, 1), timezone.datetime(current_date.year -1, 12, 31)),  # Q2: October - December previous year
        3: (timezone.datetime(current_date.year, 1, 1), timezone.datetime(current_date.year, 3, 31)),  # Q3: January - March of the following year
        4: (timezone.datetime(current_date.year, 4, 1), timezone.datetime(current_date.year, 6, 30)),  # Q4: April - June of the following year
    }
    quarter_data = {}
    # Iterate over quarters and retrieve data for each quarter
    for quarter, (start_date, end_date) in quarters.items():
        # Filter schedules for the current quarter
        quarter_schedules = Schedule.objects.filter(start_date__gte=start_date, start_date__lte=end_date)

        # Count all schedules in each district for the current quarter
        district_schedule_counts = {}
        for district in districts:
            total_schedules = quarter_schedules.filter(terminal__district=district).count()
            district_schedule_counts[district] = total_schedules

        # Count all Approved status in each district for the bank called CBE for the current quarter
        cbe_approved_counts = {}
        cbe_bank_key = "CBE"  # Replace "CBE" with the actual bank_key value
        for district in districts:
            approved_count = quarter_schedules.filter(
                terminal__district=district,
                terminal__bank_name__bank_key=cbe_bank_key,
                status=Schedule.APPROVED
            ).count()
            cbe_approved_counts[district] = approved_count

        # Calculate the percentage of approved schedules for each district for the current quarter
        district_approval_percentages = []
        for district in districts:
            total_schedules = district_schedule_counts[district]
            approved_count = cbe_approved_counts.get(district, 0)
            if total_schedules > 0:
                approval_percentage = round((approved_count / total_schedules) * 100, 2)
                district_approval_percentages.append(approval_percentage)
            else:
                district_approval_percentages.append(0)

        # Store data for the current quarter
        quarter_data[quarter] = {
            "districts": districts,
            "district_schedule_counts": district_schedule_counts,
            "cbe_approved_counts": cbe_approved_counts,
            "district_approval_percentages": district_approval_percentages
        }

    context = {
        "title": "CBE Dashboard",
        "quarter_data": quarter_data,
    }

    return render(request, 'pm/cbe_dashboard.html', context)
