from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.http import Http404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import datetime
import json
from dateutil.relativedelta import relativedelta
from pm.models import Terminal, User, Bank, Schedule
from pm.forms import TerminalForm, BankForm


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
    try:
        terminalsQuerySet = Terminal.objects.all()
        banksQuerySet = Bank.objects.all()
        numOfBanks= Bank.objects.all().count()
        numOfUsers = User.objects.all().count()
        numberOfTerminals = Terminal.objects.all().count()
        context = {
            "company": "moti Usering PLC",
            "projectName": "preventive Maintainace For ATMS",
            "terminals": terminalsQuerySet,
            'banks': banksQuerySet,
            'numOfBanks':numOfBanks,
            'numOfUsers':numOfUsers,
            'numberOfTerminals':numberOfTerminals,
        }
        return render(request, "pm/index.html", context)
    except:
        raise Http404()  # Automatically find 404.html file in golobal templates


@login_required
def user(request):
    UsersQuerySet = User.objects.all()
    context = {
        "title": "All Users",
        "users": UsersQuerySet
    }
    return render(request, 'pm/engineers.html', context)


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
def view_bank(request, id):
    bank = Bank.objects.get(pk=id)
    return HttpResponseRedirect(reverse('home'))


@login_required
def addBank(request):
    submitted = False
    if request.method == "POST":
        form = BankForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/addBank?submitted=True')
    else:
        form = BankForm
        if 'submitted' in request.GET:
            submitted = True
    context = {"form": form, "submitted": submitted}
    return render(request, 'pm/addBank.html', context)


@login_required
def updateBank(request, bank_id):
    bank = Bank.objects.get(pk=bank_id)
    form = BankForm(request.POST or None, instance=bank)
    if form.is_valid():
        form.save()
        return redirect('banks-page')
    context = {
        'bank': bank,
        'form': form,
    }
    return render(request, 'pm/update_bank.html', context)


@login_required
def terminals(request):
    try:
        terminalsQuerySet = Terminal.objects.all()
        context = {
            "title": "Terminals",
            "terminals": terminalsQuerySet,
        }
        return render(request, 'pm/terminals.html', context)
    except:
        raise Http404()


@login_required
def addTerminal(request):
    submitted = False
    if request.method == "POST":
        form = TerminalForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/add-terminal?submitted=True')
    else:
        form = TerminalForm
        if 'submitted' in request.GET:
            submitted = True
    context = {"form": form, "submitted": submitted}
    return render(request, 'pm/addTerminal.html', context)


@login_required
def schedule(request):
    try:
        scheduleQuerySet = Schedule.objects.all()
        context = {
            "title": "Scheduled ATMS",
            "schedules": scheduleQuerySet,

        }
        return render(request, 'pm/schedule.html', context)
    except:
        raise Http404()


@login_required
def reports(request):
    return render(request, 'pm/reports.html')
