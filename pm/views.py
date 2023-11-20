from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib import messages
from django.http import Http404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime, timezone
import json
from pm.models import Terminal, User, Bank, Schedule
from pm.forms import TerminalForm, BankForm, ScheduleForm, UserForm, AssignEngineerForm, EndScheduleForm


def login_user(request):
    logout(request)
    resp = {"status": 'failed', 'msg': ''}
    username = ''
    password = ''
    if request.POST:
        username = request.POST['username']
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
    return render(request, 'pm/addEngineer.html', context)


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
    if request.method == "POST":
        form = BankForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "New Bank Add Successfully!")
            return redirect('banks-page')
    else:
        form = BankForm()
    context = {"form": form, "title": "Add Bank"}
    return render(request, 'pm/addBank.html', context)


@login_required
def updateBank(request, bank_id):
    bank = Bank.objects.get(pk=bank_id)
    form = BankForm(request.POST or None, instance=bank)
    if form.is_valid():
        form.save()
        messages.info(request, "Updated Successfully!")
        return redirect('banks-page')
    context = {
        'bank': bank,
        'form': form,
        "title": "Edit Bank"
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
def schedule(request):
    scheduleQuerySet = Schedule.objects.all()
    now = datetime.now(timezone.utc)
    for schedule in scheduleQuerySet:
        schedule.remaining_day = (schedule.end_date-now).days
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
            terminals = form.cleaned_data['terminals']
            start_date =form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            description = form.cleaned_data['description']
            for terminal in terminals:
                Schedule.objects.create(
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


# @login_required
# def end_scheduled_task1(request, scheule_id):
#         schedule = Schedule.objects.get(pk=scheule_id)
#         form = EndScheduleForm(request.POST, request.FILES, instance=schedule)
#         schedule.status = "CO"
#         form.save()
#         messages.success(request, "Chenge Updated successfully!")
#         return redirect(reverse('schedules'))

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
    is_checked = False
    if request.method == "POST":
        command = request.POST
        if(command !=None):
            if(command.get("all-users")):
                users = User.objects.all()
            if(command.get('engineers')):
                users = User.objects.filter(is_moti=True)
            if(command.get('bank-users')):
                users = User.objects.filter(is_bank=True)
            if (command.get('active-users')):
                users=User.objects.filter(is_active=True)
            if (command.get('inactive-users')):
                users = User.objects.filter(is_active=False)
            if (command.get('super-users')):
                users = User.objects.filter(is_staff=True)

    context = {
        "users": users,
        "is_checked":is_checked,
        "title":"Users Report",
    }
    return render(request, 'pm/engineers_report.html', context)

def banks_list(request):
    all_banks = Bank.objects.all()
    active_banks = Bank.objects.filter(is_active=True)
    inactive_banks = Bank.objects.filter(is_active=False)
    
        
    context = {
        "banks": all_banks,
        "title": "Banks Report",
    }
    return render(request, 'pm/banks_report.html', context)


def terminals_list(request):
    all_terminals = Terminal.objects.all()
    north_terminals = Terminal.objects.filter(moti_district="NR")
    south_terminals = Terminal.objects.filter(moti_district="SR")
    east_terminals = Terminal.objects.filter(moti_district="ER")
    west_terminals = Terminal.objects.filter(moti_district="WR")
    centeral_terminals = Terminal.objects.filter(moti_district="CR")
    context = {
        "terminals": all_terminals,
        "title": "Terminals Report",
    }
    return render(request, 'pm/terminals_report.html', context)


def schedule_list(request):
    all_schedules = Schedule.objects.all()
    pending_schedules = Schedule.objects.filter(status="PE")
    waiting_tasks = Schedule.objects.filter(status="WT")
    onprogress_tasks = Schedule.objects.filter(status="OP")
    completed_tasks = Schedule.objects.filter(status="CO")
    context = {
        "schedules": all_schedules,
        "title": "Scheduls Report",
    }
    return render(request, 'pm/schedules_report.html', context)
