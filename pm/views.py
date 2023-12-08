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
from pm.forms import TerminalForm, BankForm, ScheduleForm, UserForm, AssignEngineerForm, EndScheduleForm,ApprovalScheduleForm,AllScheduleForm



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
    }
    return render(request, 'pm/schedule.html', context)


def detail_schedules_list(request, pk):
    schedule = get_object_or_404(AllSchedule, pk=pk)
    schedules_list = Schedule.objects.filter(schedule=schedule)
    specific_schedule_count = Schedule.objects.filter(schedule=schedule).count()
    pending_schedule = schedules_list.filter(status="PE").count()
    waiting_schedule = schedules_list.filter(status="WT").count()
    onprogress_schedule = schedules_list.filter(status="OP").count()
    submitted_schedule = schedules_list.filter(status="SB").count()
    approved_schedule = schedules_list.filter(status="AP").count()
    rejected_schedule = schedules_list.filter(status="RE").count()

    # calculating Pending , waiting, onprogress and completed rate
    pending_rate = round(pending_schedule/specific_schedule_count,1)*100
    waiting_rate = round(waiting_schedule/specific_schedule_count,1)*100
    onprogress_rate = round(onprogress_schedule/specific_schedule_count,1)*100
    submitted_rate = round(submitted_schedule/specific_schedule_count, 1)*100
    approved_rate = round(approved_schedule/specific_schedule_count,1)*100
    rejected_rate = round(rejected_schedule/specific_schedule_count,1)*100

    engineer_nedded = math.ceil(pending_schedule/7)
    # Calcuate Remaining Days
    now = datetime.now(timezone.utc)
    for schedule in schedules_list:
        schedule.remaining_days = (schedule.end_date - now).days 
        
    context = {
        'schedules': schedules_list,
        "title": "Detial shedule",
        "pending_rate": pending_rate,
        "waiting_rate": waiting_rate,
        "onprogress_rate": onprogress_rate,
        "submitted_rate": submitted_rate,
        "approved_rate":approved_rate,
        "rejected_rate":rejected_rate,
        "all_schedule_count": specific_schedule_count,
        "engineer_nedded": engineer_nedded,
        
    }
    return render(request, 'pm/detail_schedules_list.html', context)


@login_required
def create_schedule(request):
    tqs = Terminal.objects.all()
    if request.method == 'POST':
        form = ScheduleForm(request.POST)
        form1 = AllScheduleForm(request.POST)
        if form.is_valid() and form1.is_valid():
            form1.clean()
            form1_instance = form1.save()
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
            messages.success(request, "Chenge Updated successfully!")
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
        form = ApprovalScheduleForm(request.POST, request.FILES, instance=schedule)
        if form.is_valid():
            schedule.status = "AP"
            form.save()
            messages.success(request, "Chenge Updated successfully!")
            return redirect(f'/detail_schedule/{all_schedule_id}')
    else:
        schedule = Schedule.objects.get(pk=id)
        form = ApprovalScheduleForm(instance=schedule)
        all_schedule_id = schedule.schedule.id
    context = {'form': form, 'schedule': schedule, "title": "Approval task","all_schedule_id":all_schedule_id}
    return render(request, 'pm/approve_task.html', context)

def reject_task(request, id):
    if request.method == 'POST':
        schedule = Schedule.objects.get(pk=id)
        all_schedule_id = schedule.schedule.id
         
        form = ApprovalScheduleForm(request.POST, request.FILES, instance=schedule)
        if form.is_valid():
            schedule.status = "RE"
            form.save()
            messages.success(request, "Chenge Updated successfully!")
            return redirect(f'/detail_schedule/{all_schedule_id}')
    else:
        schedule = Schedule.objects.get(pk=id)
        form = ApprovalScheduleForm(instance=schedule)
        all_schedule_id = schedule.schedule.id
    context = {'form': form, 'schedule': schedule, "title": "Reject task","all_schedule_id":all_schedule_id}
    return render(request, 'pm/reject_task.html', context)


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
    from_date = request.POST.get('from_date')
    to_date = request.POST.get('to_date')
    if (selected == 'All users'):
        users = User.objects.filter(date_joined__range=(from_date, to_date))
        title = "All Users"
    if (selected == 'Engineers'):
        users = User.objects.filter(
            is_engineer=True, date_joined__range=(from_date, to_date))
        title = "Engineers"
    if (selected == 'Active Users'):
        users = User.objects.filter(
            is_active=True, date_joined__range=(from_date, to_date))
        title = "Active Users"
    if (selected == 'InActive Users'):
        users = User.objects.filter(
            is_active=False, date_joined__range=(from_date, to_date))
        title ="InActive Users"
    if (selected == 'Super Users'):
        users = User.objects.filter(
            is_super_user=True, date_joined__range=(from_date, to_date))
        title="Super Users"
    if (selected == 'Bank Users'):
        users = User.objects.filter(
            is_bank_user=True, created_date__range=(from_date, to_date))
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
    from_date = request.POST.get('from_date')
    to_date = request.POST.get('to_date')
    if (selected == 'All Banks'):
        banks = Bank.objects.filter(created_date__range=(from_date,to_date))
        title ="All Banks"
    if(selected =='Active Banks'):
        banks = Bank.objects.filter(is_active=True, created_date__range=(from_date,to_date))
        title = "Active Banks"
    if(selected == 'InActive Banks'):
        banks = Bank.objects.filter(is_active=False, created_date__range=(from_date,to_date))
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
    from_date = request.POST.get('from_date')
    to_date = request.POST.get('to_date')
    if(selected == "All Terminals"):
        terminals = Terminal.objects.filter(
            created_date__range=(from_date, to_date))
        title ="All Terminals"
    if(selected == "North Terminals"):
        terminals = Terminal.objects.filter(
            moti_district="NR", created_date__range=(from_date, to_date))
        title = "North Terminals"
    if(selected == "South Terminals"):
        terminals = Terminal.objects.filter(
            moti_district="SR", created_date__range=(from_date, to_date))
        title = "South Terminals"
    if(selected == "Centeral Terminals"):
        terminals = Terminal.objects.filter(
            moti_district="CR", created_date__range=(from_date, to_date))
        title ="Centeral Terminals"
    if(selected =="East Terminals"):
        terminals = Terminal.objects.filter(
            moti_district="ER", created_date__range=(from_date, to_date))
        title ="East Terminals"
    if(selected == "West Terminals"):
        terminals = Terminal.objects.filter(
            moti_district="WR", created_date__range=(from_date, to_date))
        title = "West Terminals"

    context = {
        "terminals": terminals,
        "title": title,
        "selected": selected
    }
    return render(request, 'pm/terminals_report.html', context)

@login_required
def schedule_list(request):
    title = "Schedules Report"
    banks = Bank.objects.all()
    schedules = Schedule.objects.all()
    bank_name = request.POST.get('options')
    print(f'form bank_id {bank_name}')
    # print(bank_id)
    for s in schedules:
       
           print(f'form loop{ s.terminal.bank_name}')

    selected= False

    context = {
        "schedules": schedules,
        "title": title,
        "selected": selected,
        'banks': banks,
    }
    return render(request, 'pm/schedules_report.html', context)
