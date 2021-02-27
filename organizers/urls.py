from django.urls import path,include
from organizers.views import *
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', complete, name='complete'),
    path('organizerform/', organizerform ,name="organizer-form"),
    path('dashboard/',dashboard, name="dashboard"),
    path('dashboard/<int:id>/', organapp, name="organ-appointment")
    #path('dashboard/', dashboard, name='dashboard')
]