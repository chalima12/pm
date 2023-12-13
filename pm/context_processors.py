from .models import Schedule, User
import json


def global_context(request):
    #TODO: Context Passed form Schedule LIst and 
    logged_in_user = request.user
    pendingSchedule = Schedule.objects.filter(status="PE").count()
    waitingSchedule = Schedule.objects.filter(status="WT").count()
    onprogressSchedule = Schedule.objects.filter(status="OP").count()
    submittedSchedule = Schedule.objects.filter(status="SB").count()
    approvedSchedule = Schedule.objects.filter(status="AP").count()
    rejectedSchedule = Schedule.objects.filter(status="RE").count()
    
    allSchedule = pendingSchedule + waitingSchedule + onprogressSchedule + submittedSchedule + approvedSchedule + rejectedSchedule
    context = {
        "allSchedule":allSchedule,
        "pendingSchedule": json.dumps(pendingSchedule),
        "waitingSchedule": json.dumps(waitingSchedule),
        "onprogressSchedule": json.dumps(onprogressSchedule),
        "submittedSchedule": json.dumps(submittedSchedule),
        "approvedSchedule": json.dumps(approvedSchedule),
        "rejectedSchedule": json.dumps(rejectedSchedule),
        "logged_in_user":logged_in_user,
    }
    return context 
    
