from .models import Schedule,Bank


def global_context(request):
    onprogressSchedule = Schedule.objects.filter(status="OP").count()
    commpletedSchedule = Schedule.objects.filter(status ="CO").count()
    pendingSchedule = Schedule.objects.filter(status="PE").count()
    allSchedule = onprogressSchedule+commpletedSchedule+pendingSchedule
    context = {
        "allSchedule":allSchedule,
        "pendingSchedule": pendingSchedule,
        "onprogressSchedule":onprogressSchedule,
        "commpletedSchedule":commpletedSchedule,

    }
    return context
