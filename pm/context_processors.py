from .models import Schedule
from django.contrib import messages
import json


def global_context(request):
    onprogressSchedule = Schedule.objects.filter(status="OP").count()
    commpletedSchedule = Schedule.objects.filter(status ="CO").count()
    pendingSchedule = Schedule.objects.filter(status="PE").count()
    waitingSchedule = Schedule.objects.filter(status="WT").count()
    allSchedule = onprogressSchedule+commpletedSchedule+pendingSchedule+waitingSchedule
    context = {
        "allSchedule":allSchedule,
        "pendingSchedule": json.dumps(pendingSchedule),
        "waitingSchedule": json.dumps(waitingSchedule),
        "onprogressSchedule": json.dumps(onprogressSchedule),
        "commpletedSchedule": json.dumps(commpletedSchedule),
        "messages":messages

    }
    return context
