from django.shortcuts import render,redirect
from django.http import Http404
import datetime
from dateutil.relativedelta import relativedelta
from pm.models import Terminal, Engineer, Bank, Schedule
from pm.forms import TerminalForm
# Create your views here.

a = '2014-05-06 12:00:56'
b = '2014-02-06 16:08:22'
start = datetime.datetime.strptime(a, '%Y-%m-%d %H:%M:%S')
ends = datetime.datetime.strptime(b, '%Y-%m-%d %H:%M:%S')
diff = relativedelta(start, ends)
# print(diff.years, diff.months, diff.days,
#       diff.hours, diff.minutes, diff.seconds)
month = diff.months
day = diff.days
hour = diff.hours

# Futer Reference 
# import datetime
# from dateutil.relativedelta import relativedelta
# print(datetime.datetime.now())
# a = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
# b = '2020-03-06 16:08:22'
# start = datetime.datetime.strptime(a, '%Y-%m-%d %H:%M:%S')
# ends = datetime.datetime.strptime(b, '%Y-%m-%d %H:%M:%S')
# diff = relativedelta(start, ends)
# print (diff.years, diff.months, diff.days, diff.hours, diff.minutes)


def home(request):
    try:
        terminalsQuerySet = Terminal.objects.all()
        context = {
            "company": "moti Engineering PLC",
            "projectName": "preventive Maintainace For ATMS",
            "terminals": terminalsQuerySet,
            "month": month,
            "day": day,
            "hour":hour,
        }
        return render(request, "pm/index.html", context)
    except:
        raise Http404()  # Automatically find 404.html file in golobal templates


def engineers(request):
    engineersQuerySet = Engineer.objects.all()
    context = {
        "title": "All Engineers",
        "engineers": engineersQuerySet
    }
    return render(request, 'pm/engineers.html', context)


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
        "form":form,
    }
    return render(request,"pm/terminalForm.html",context)

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


def reports(request):
    return render(request, 'pm/reports.html')
