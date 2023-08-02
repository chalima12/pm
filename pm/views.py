from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
    return HttpResponse("Moti Engineering")

def allBanks(request):
    return HttpResponse("All Banks")

def atms(request):
    return HttpResponse("Atms")

def makeSchedule():
    return HttpResponse("All done")