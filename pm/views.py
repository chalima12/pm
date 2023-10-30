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
    terminalsQuerySet = Terminal.objects.all().order_by('tid')[:10]
    banksQuerySet = Bank.objects.all()
    numOfBanks = Bank.objects.all().count()
    numOfUsers = User.objects.all().count()
    numberofTerminals = Terminal.objects.all().count()
    pendingTerminals = Schedule.objects.filter(status="PE").count()
    pendingLists = Schedule.objects.filter(status="PE").all()
    # cleanedTerminals = Schedule.objects.filter(status="CO").count()
    context = {
        "company": "moti Usering PLC",
        "projectName": "preventive Maintainace For ATMS",
        "terminals": terminalsQuerySet,
        'banks': banksQuerySet,
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
    return HttpResponseRedirect(reverse('index'))


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
    context = {'form': form}
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
    context = {"form": form}
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
    }
    return render(request, 'pm/update_bank.html', context)


@login_required
def deactivate_bank(request, bank_id):
    bank = Bank.objects.get(pk=bank_id)
    bank.is_active = False
    bank.save()
    return HttpResponseRedirect(reverse('banks-page'))


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
    context = {"form": form}
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
    if request.method == 'POST':
        form = ScheduleForm(request.POST)
        if form.is_valid():
            
            terminals =form.cleaned_data['terminals']
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            description = form.cleaned_data['description']

            for terminal in terminals:
                Schedule.objects.create(
                    terminal_name = terminal,
                    start_date=start_date,
                    end_date=end_date,
                    description =description,
                )
                form.save_m2m()
                messages.success(request, "Schedules created successfully!")
                return redirect('schedules')
    else:
        form = ScheduleForm()

    return render(request, 'pm/addSchedule.html', {'form': form})

# @login_required
# def create_meeting_schedule(request):
#     if request.method == 'POST':
#         form = MeetingScheduleForm(request.POST)
#         if form.is_valid():
#             users = form.cleaned_data['users']
#             start_date = form.cleaned_data['start_date']
#             end_date = form.cleaned_data['end_date']
#             remark = form.cleaned_data['remark']

#             for user in users:
#                 Meeting_Schedule.objects.create(
#                     user=user,
#                     start_date=start_date,
#                     end_date=end_date,
#                     remark=remark,
#                     status=True
#                 )

#             messages.success(request, "Meeting schedules created successfully!")
#             return redirect('create_meeting_schedule')
#     else:
#         form = MeetingScheduleForm()

#     return render(request, 'meeting_schedule.html', {'form': form})

@login_required
def assign_engineer(request, id):
    if request.method == 'POST':
        schedule = Schedule.objects.get(pk=id)
        form = AssignEngineerForm(request.POST, instance=schedule)
        if form.is_valid():
            schedule.status = "OP"
            form.save()
            messages.success(request, "Engineer Assigned successfully!")
            return redirect('schedules')
    else:
        schedule = Schedule.objects.get(pk=id)
        form = AssignEngineerForm(instance=schedule)
    context = {'form': form, 'schedule': schedule}
    return render(request, 'pm/assign_engineer.html', context)


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
    context = {'form': form, 'schedule': schedule}
    return render(request, 'pm/end_schedule.html', context)

@ login_required
def filter(request):
    tQs= ''
    terminal = request.GET.get('terminals')
    if terminal !='' and terminal is not None:
        tQs = Terminal.objects.all()
    return tQs
@login_required
def reports(request):
    terminals = filter(request)
    context = {
        "terminals":terminals
    }
    return render(request, 'pm/reports.html',context)

