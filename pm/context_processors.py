from .models import Schedule, User
import json


def global_context(request):
    #TODO: Context Passed form Schedule LIst and 
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
    }
    return context 
    
