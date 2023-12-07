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




# Schedlule 96------
                        # <a href=" {% url "assign-engineer" schedule.id %}"
                        #   style="width: 90px"
                        #   class="d-inline p-2 m-2 btn btn-block btn-outline-info"
                        #   ><i class="fa">Chenge</i></a>
                        # <a href="{% url "end-task" schedule.id %}"
                        #   style="width: 90px"
                        #   class="d-inline p-2 m-3 btn btn-block btn-danger"
                        #   ><i class="fa">End</i></a>



# {% load static %}
# <!--Login Form-->
# <!DOCTYPE html>
# <html lang="en">
# <head>
#   <meta charset="utf-8">
#   <meta name="viewport" content="width=device-width, initial-scale=1">
#   <title>Moti Engineering</title>

#   <!-- Google Font: Source Sans Pro -->
#   <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Source+Sans+Pro:300,400,400i,700&display=fallback">
#   <!-- Font Awesome -->
#   <link rel="stylesheet" href="{% static "plugins/fontawesome-free/css/all.min.css" %}">
#   <!-- icheck bootstrap -->
#   <link rel="stylesheet" href="{% static "plugins/icheck-bootstrap/icheck-bootstrap.min.css" %}">
#   <!-- Theme style -->
#   <link rel="stylesheet" href="{% static "dist/css/adminlte.min.css" %}">
# </head>
# <body class="hold-transition login-page">
# <div class="login-box" >
#   <h1>Moti Engineering</h1>
#       </div>
#   <div class="card card-outline card-success">
#     <div class="card-header text-center">
#       <h2>PM Portal</h2>
#     </div>
#     <div class="card-body">
#       <p class="login-box-msg">Sign in to start your session</p>

#       <form action="" method="post">
#         {% csrf_token %}
#         <div class="row px-5 ">
#           <div class = "col-10">
#               {{form.as_p}}
#           </div>
#           <!-- /.col -->
#          {{form.password}}
#          {{form.username}}
#           <!-- /.col -->
#         </div>
#          <div class="col-12">
#             <button type="submit" class="btn btn-primary btn-block" style="background-color: rgb(114, 231, 141);color: black;">Sign In</button>
#           </div>
#       </form>
#     </div>

#     <!-- /.card-body -->
#   </div>
#   <!-- /.card -->
#       <div class ="card-footer text-black display-5 ">
# <p>THE LEADING IT & BANKING AUTOMATION SOLUTION PROVIDER IN ETHIOPIA</p>
#     </div>
# </div>
# <!-- /.login-box -->

# <!-- jQuery -->
# <script src="{% static "plugins/jquery/jquery.min.js" %}"></script>
# <!-- Bootstrap 4 -->
# <script src="{% static "plugins/bootstrap/js/bootstrap.bundle.min.js" %}"></script>
# <!-- AdminLTE App -->
# <script src="{% static "dist/js/adminlte.min.js" %}"></script>
# </body>
# </html>




print(selected_bank_name)

    if selected_bank_name:
        selected_bank = banks.filter(bank_name=selected_bank_name).first()
        print(selected_bank)

        if selected_bank:
            schedules = Bank.objects.filter(bank_name=selected_bank)
            print(schedules)
            selected = True
        else:
            schedules = Schedule.objects.none()
    else:
        schedules = Schedule.objects.all()
        selected = False

# {% comment %} <div class="form-group">
#                         <label>Filter Schedules Form the Dropdown</label>
#                         <select class="form-control" name ="options">
#                           <option value ="0"selected >-----Select-----</option>
#                           <option value ="All Schedule" >All Schedules</option>
#                           <option value ="Pending Schedule" >Pending Schedules</option>
#                           <option value ="Waiting Task" >Waiting Task</option>  
#                           <option value ="OnProgress Task" >OnProgress Task</option>  
#                           <option value ="Completed Task" >Completed Task</option>  
#                         </select>
#                       </div> {% endcomment %}

@login_required
def schedule_list(request):
    schedules = Schedule.objects.all()
    title = "Schedules Report"
    banks = Bank.objects.all()
    selected = False
    selected_bank = request.POST.get('options')
    for s in schedules:

        if selected_bank == s.terminal.bank_name.bank_name:
            bank_id = s.terminal.bank_name.id
            schedules = Schedule.objects.filter(bank_name_id=bank_id)
            print(schedules)
        #    print(selected_bank)
    # if selected_bank:
    #     schedules = Schedule.objects.filter(bank_name=selected_bank)

    # print(schedules)
    # selected = request.POST.get('options')
    # selected_bank = request.POST.get('options')
    # print(f"Selected ----------- {selected} :Selected Bank --------- {selected_bank}")
    # from_date = request.POST.get('from_date')
    # to_date = request.POST.get('to_date')
    # if selected_bank:
    #     schedules = Schedule.objects.filter(
    #         bank_name=selected_bank,
    #         created_date__range=(from_date, to_date)
    #     )
    #     title = f"Schedules for {selected_bank}"
    # if(selected == "All Schedule"):
    #     schedules = Schedule.objects.filter(
    #         created_date__range=(from_date, to_date))
    #     title = "All Tasks"
    # if(selected =="Pending Schedule"):
    #     schedules = Schedule.objects.filter(
    #         status="PE", created_date__range=(from_date, to_date))
    #     title = "Pending Schedule"
    # if(selected == "Waiting Task"):
    #     schedules = Schedule.objects.filter(
    #         status="WT", created_date__range=(from_date, to_date))
    #     title = "Waiting Task"
    # if(selected == "OnProgress Task"):
    #     schedules = Schedule.objects.filter(
    #         status="OP", created_date__range=(from_date, to_date))
    #     title = "OnProgress Task"
    # if(selected == "Completed Task"):
    #     schedules = Schedule.objects.filter(
    #         status="SB", created_date__range=(from_date, to_date))
    #     title ="Completed Task"
    context = {
        "schedules": schedules,
        "title": title,
        "selected": selected,
        'banks': banks,
    }
    return render(request, 'pm/schedules_report.html', context)
