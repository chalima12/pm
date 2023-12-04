from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib import messages
from django.http import Http404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime, timezone,timedelta,date
from django.db.models import Q
import json, math
from pm.models import Terminal, User, Bank, Schedule,AllSchedule
from pm.forms import TerminalForm, BankForm, ScheduleForm, UserForm, AssignEngineerForm, EndScheduleForm



def login_user(request):
    logout(request)
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
    numOfBanks = Bank.objects.all().count()
    numOfUsers = User.objects.all().count()
    numberofTerminals = Terminal.objects.all().count()
    pendingTerminals = Schedule.objects.filter(status="PE").count()
    pendingLists = Schedule.objects.filter(status="PE").all()
    # cleanedTerminals = Schedule.objects.filter(status="CO").count()
    context = {
        "company": "Moti Engineering PLC",
        "projectName": "Preventive Maintainace For ATMS",
        'title':"Dashboard",
        'numOfBanks': numOfBanks,
        'numOfUsers': numOfUsers,
        'numberofTerminals': numberofTerminals,
        "pendingTerminals": pendingTerminals,
        "pendingLists": pendingLists
    }
    return render(request, "pm/index.html", context)


@login_required
def user(request):
    UsersQuerySet = User.objects.all()
    context = {
        "title": "All Users",
        "users": UsersQuerySet
    }
    return render(request, 'pm/engineers.html', context)


def view_user(request, id):
    return HttpResponseRedirect(reverse('all-engineers'))


@login_required
def create_user(request):
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
    form = UserForm(request.POST or None, instance=user)
    if form.is_valid():
        form.save()
        messages.info(request, "Updated Successfully!")
        return redirect('all-engineers')
    context = {
        'user': user,
        'form': form,
        "title": "edit User"
    }
    return render(request, 'pm/update_user.html', context)


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
        # "count":count
    }
    return render(request, 'pm/schedule.html', context)


def detail_schedules_list(request, scheule_id):
    schedule = get_object_or_404(AllSchedule, pk=scheule_id)
    schedules_list = Schedule.objects.filter(schedule=schedule)
    specific_schedule_count = Schedule.objects.filter(schedule=schedule).count()
    pending_schedule = schedules_list.filter(status="PE").count()
    waiting_schedule = schedules_list.filter(status="WT").count()
    onprogress_schedule = schedules_list.filter(status="OP").count()
    completed_schedule = schedules_list.filter(status="CO").count()
    # calculating Pending , waiting, onprogress and completed rate
    pending_rate = round(pending_schedule/specific_schedule_count,2)*100
    waiting_rate = round(waiting_schedule/specific_schedule_count,2)*100
    onprogress_rate = round(onprogress_schedule/specific_schedule_count,2)*100
    completed_rate = round(completed_schedule/specific_schedule_count,2)*100
    engineer_nedded = math.ceil(pending_schedule/7)
    # Calcuate Remaining Days
    now = datetime.now(timezone.utc)
    for schedule in schedules_list:
        if now< schedule.start_date:
            schedule.remaining_days =(schedule.start_date -now).days
        else:
            days_elapsed = (now - schedule.start_date).days
            schedule.remaining_days = max(0, 90 - (days_elapsed % 90))
            print(schedule.remaining_days)
    context = {
        'schedules': schedules_list,
        "title": "Detial shedule",
        "pending_rate": pending_rate,
        "waiting_rate": waiting_rate,
        "onprogress_rate": onprogress_rate,
        "completed_rate": completed_rate,
        "all_schedule_count": specific_schedule_count,
        "engineer_nedded": engineer_nedded,
        
    }
    return render(request, 'pm/detail_schedules_list.html', context)

@login_required
def schedule(request):
    scheduleQuerySet = Schedule.objects.all()
    # now = datetime.now(timezone.utc)
    one_day = timedelta(days=1)
    for schedule in scheduleQuerySet:
        schedule.remaining_day = (
            (schedule.end_date-schedule.start_date)).days
    context = {
        "title": "Scheduled ATMS",
        "schedules": scheduleQuerySet,
    }
    return render(request, 'pm/schedule.html', context)


@login_required
def create_schedule(request):
    tqs = Terminal.objects.all()
    if request.method == 'POST':
        form = ScheduleForm(request.POST)
        if form.is_valid():
            schedule = form.cleaned_data['schedule']
            terminals = form.cleaned_data['terminals']
            start_date =form.cleaned_data['start_date']
            string_start_date = str(date.isoformat(start_date))
            formated_start_date = datetime.strptime(string_start_date, "%Y-%m-%d")
            # print(f"Start Date: {formated_start_date}")
            end_date = formated_start_date + timedelta(days=90) #TODO: make days select form user 3, 4 or 6 month
            description = form.cleaned_data['description']
            for terminal in terminals:
                Schedule.objects.create(
                    schedule=schedule,
                    terminal=terminal,
                    start_date=start_date,
                    end_date=end_date,
                    description=description,
                )

            messages.success(request, "Schedules created successfully!")
            return redirect('schedules')
    else:
        form =ScheduleForm()
    return render(request, 'pm/addSchedule.html', {'form': form,"terminals":tqs})


@login_required
def assign_engineer(request, id):
    if request.method == 'POST':
        schedule = Schedule.objects.get(pk=id)
        form = AssignEngineerForm(request.POST, instance=schedule)
        if form.is_valid():
            schedule.status = "WT"
            form.save()
            messages.success(request, "Engineer Assigned successfully!")
            return redirect('schedules')
    else:
        schedule = Schedule.objects.get(pk=id)
        form = AssignEngineerForm(instance=schedule)
    context = {'form': form,
            'schedule': schedule,
            "title": "Assign Engineer"
            }
    return render(request, 'pm/assign_engineer.html', context)


def start_task(request, scheule_id):
    schedule = Schedule.objects.get(pk=scheule_id)
    schedule.status = "OP"
    schedule.save()
    return redirect(reverse('schedules'))
@login_required
def end_scheduled_task(request, id):
    if request.method == 'POST':
        schedule = Schedule.objects.get(pk=id)
        form = EndScheduleForm(request.POST, request.FILES, instance=schedule)
        if form.is_valid():
            schedule.status = "CO"
            form.save()
            messages.success(request, "Chenge Updated successfully!")
            return redirect('schedules')
    else:
        schedule = Schedule.objects.get(pk=id)
        form = EndScheduleForm(instance=schedule)
    context = {'form': form, 'schedule': schedule, "title": "End task"}
    return render(request, 'pm/end_schedule.html', context)


@ login_required
def filter(request):
    tQs = ''
    terminal = request.GET.get('terminals')
    if terminal != '' and terminal is not None:
        tQs = Terminal.objects.all()
    return tQs


@login_required
def reports(request):
    terminals = filter(request)
    context = {
        "terminals": terminals
    }
    return render(request, 'pm/reports.html', context)

# Reports View


@login_required
def engineers_list(request):
    users = None
    title = "Users Report"
    selected = request.POST.get('options')
    if (selected == 'All users'):
        users= User.objects.all()
        title = "All Users"
    if (selected == 'Engineers'):
        users = User.objects.filter(is_engineer=True)
        title = "Engineers"
    if (selected == 'Active Users'):
        users = User.objects.filter(is_active=True)
        title = "Active Users"
    if (selected == 'InActive Users'):
        users = User.objects.filter(is_active=False)
        title ="InActive Users"
    if (selected == 'Super Users'):
        users = User.objects.filter(is_super_user=True)
        title="Super Users"
    if (selected == 'Bank Users'):
        users = User.objects.filter(is_bank_user=True)
        title = "Bank Users"
    context = {
        "users": users,
        "title":title,
        'selected':selected
        
    }
    return render(request, 'pm/engineers_report.html', context)

def banks_list(request):
    banks = None
    title = "Banks Report"
    selected = request.POST.get('options')
    if (selected == 'All Banks'):
        banks = Bank.objects.all()
        title ="All Banks"
    if(selected =='Active Banks'):
        banks = Bank.objects.filter(is_active=True)
        title = "Active Banks"
    if(selected == 'InActive Banks'):
        banks = Bank.objects.filter(is_active=False)
        title = "InActive Banks"
    context = {
        "banks": banks,
        "title": title,
        "selected": selected
    }
    return render(request, 'pm/banks_report.html', context)


def terminals_list(request):
    terminals = None
    title = "Terminals Report"
    selected = request.POST.get('options')
    if(selected == "All Terminals"):
        terminals =Terminal.objects.all()
        title ="All Terminals"
    if(selected == "North Terminals"):
        terminals = Terminal.objects.filter(moti_district="NR")
        title = "North Terminals"
    if(selected == "South Terminals"):
        terminals=Terminal.objects.filter(moti_district="SR")
        title = "South Terminals"
    if(selected == "Centeral Terminals"):
        terminals = Terminal.objects.filter(moti_district="CR")
        title ="Centeral Terminals"
    if(selected =="East Terminals"):
        terminals = Terminal.objects.filter(moti_district="ER")
        title ="East Terminals"
    if(selected == "West Terminals"):
        terminals = Terminal.objects.filter(moti_district="WR")
        title = "West Terminals"

    context = {
        "terminals": terminals,
        "title": title,
        "selected": selected
    }
    return render(request, 'pm/terminals_report.html', context)


def schedule_list(request):
    schedules = None
    title = "Schedules Report"
    selected = request.POST.get('options')
    if(selected == "All Schedule"):
        schedules = Schedule.objects.all()
        title = "All Tasks"
    if(selected =="Pending Schedule"):
        schedules = Schedule.objects.filter(status="PE")
        title = "Pending Schedule"
    if(selected == "Waiting Task"):
        schedules = Schedule.objects.filter(status="WT")
        title = "Waiting Task"
    if(selected == "OnProgress Task"):
        schedules = Schedule.objects.filter(status="OP")
        title = "OnProgress Task"
    if(selected == "Completed Task"):
        schedules = Schedule.objects.filter(status="CO")
        title ="Completed Task"
    context = {
        "schedules": schedules,
        "title": title,
        "selected": selected,
    }
    return render(request, 'pm/schedules_report.html', context)
