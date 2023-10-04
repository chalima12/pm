# Django rest framework Imports
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# Create your views here.

a = '2014-05-06 12:00:56'
b = '2014-02-06 16:08:22'
start = datetime.datetime.strptime(a, '%Y-%m-%d %H:%M:%S')
ends = datetime.datetime.strptime(b, '%Y-%m-%d %H:%M:%S')
diff = relativedelta(start, ends)
# print(diff.years, diff.months, diff.days,
#       diff.hours, diff.minutes, diff.seconds)
month = diff.months
day = diff.days
hour = diff.hours

# Futer Reference
# import datetime
# from dateutil.relativedelta import relativedelta
# print(datetime.datetime.now())
# a = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
# b = '2020-03-06 16:08:22'
# start = datetime.datetime.strptime(a, '%Y-%m-%d %H:%M:%S')
# ends = datetime.datetime.strptime(b, '%Y-%m-%d %H:%M:%S')
# diff = relativedelta(start, ends)
# print (diff.years, diff.months, diff.days, diff.hours, diff.minutes)

# Rest Framwork  Implementations

# @api_view()
# def terminal_list(request):
#     return Response('ok')

# @api_view()
# def terminal_detail(request,id):
#     return Response(id)
# Simple django implementions


# def login(request):
#     return render(request, 'registration/login.html')

# Login