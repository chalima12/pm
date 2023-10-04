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
        context = {
            "company": "moti Usering PLC",
            "projectName": "preventive Maintainace For ATMS",
            "terminals": terminalsQuerySet,
        }
        return render(request, "pm/index.html", context)
    except:
        raise Http404()  # Automatically find 404.html file in golobal templates


@login_required
def user(request):
    UsersQuerySet = User.objects.all()
    context = {
        "title": "All Users",
        "Users": UsersQuerySet
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
    if request.method == "POST":
        form = BankForm(request.POST)
        if form.is_valid():
            new_bank_name = form.cleaned_data['bank_name']
            new_bank_key = form.cleaned_data['bank_key']
            new_bank = Bank(bank_name=new_bank_name, bank_key=new_bank_key)
            new_bank.save()

            context = {
                "form": BankForm(),
                "success": True
            }
            return redirect(reverse('pm/addBank.html', context))
    else:
        form = BankForm()
        return render(request, 'pm/addBank.html', {"form": form})


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
    if request.method == "POST":
        form = TerminalForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('/add-terminal')
            except:
                print("ERROR Happend")

    else:
        form = TerminalForm()
    context = {
        "form": form,
    }
    return render(request, "pm/terminalForm.html", context)


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
