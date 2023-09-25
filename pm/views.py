from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
import json
# Create your views here.


def home(request):
    try:
        context = {
            "company": "moti Engineering PLC",
            "projectName": "preventive Maintainace For ATMS"}
        return render(request, "pm/index.html", context)
    except:
        raise Http404()  # Automatically find 404.html file in golobal templates


def engineers(request):
    return render(request, 'pm/engineers.html')


def banks(request):
    return render(request, 'pm/banks.html')


def terminals(request):
    return render(request, 'pm/terminals.html')


def schedule(request):
    return render(request, 'pm/schedule.html')


def reports(request):
    return render(request, 'pm/reports.html')
