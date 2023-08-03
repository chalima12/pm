from django.shortcuts import render
from django.http import HttpResponse,Http404

# Create your views here.

def home(request):
    try:
        context ={
        "company":"moti Engineering PLC",
        "projectName":"preventive Maintainace For ATMS"}
        return render(request,"pm/home.html",context)
    except:
        raise Http404() # Automatically find 404.html file in golobal templates 
        


def allBanks(request):
    return HttpResponse("All Banks")

def atms(request):
    return HttpResponse("Atms")

def makeSchedule(request):
    return HttpResponse("All done")