from django.urls import path
from . import views
urlpatterns = [
    path('', views.home),
    path('Banks', views.allBanks),
    path('Atms',views.atms),
    path('Schedule',views.makeSchedule)
]
