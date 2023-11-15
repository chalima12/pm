from .models import Schedule
import json


def global_context(request):
    onprogressSchedule = Schedule.objects.filter(status="OP").count()
    commpletedSchedule = Schedule.objects.filter(status ="CO").count()
    pendingSchedule = Schedule.objects.filter(status="PE").count()
    waitingSchedule = Schedule.objects.filter(status="WT").count()
    allSchedule = onprogressSchedule+commpletedSchedule+pendingSchedule
    context = {
        "allSchedule":allSchedule,
        "pendingSchedule": json.dumps(pendingSchedule),
        "waitingSchedule": json.dumps(waitingSchedule),
        "onprogressSchedule": json.dumps(onprogressSchedule),
        "commpletedSchedule": json.dumps(commpletedSchedule),

    }
    return context
