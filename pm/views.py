from django.shortcuts import render
from django.http import Http404

from pm.models import Terminal, Engineer, Bank, Schedule
# Create your views here.


def home(request):
    try:
        terminalsQuerySet = Terminal.objects.all()
        context = {
            "company": "moti Engineering PLC",
            "projectName": "preventive Maintainace For ATMS",
            "terminals":terminalsQuerySet
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
