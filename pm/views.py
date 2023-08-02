from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def home(request):
    context ={
        "company":"moti Engineering PLC",
        "projectName":"preventive Maintainace For ATMS"
    }
    return render(request,"pm/home.html",context)

def allBanks(request):
    return HttpResponse("All Banks")

def atms(request):
    return HttpResponse("Atms")

def makeSchedule(request):
    return HttpResponse("All done")