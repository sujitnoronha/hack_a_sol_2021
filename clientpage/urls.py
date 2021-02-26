from django.urls import path,include
from clientpage.views import *

urlpatterns = [
    path('', home, name='home'),
    path('<int:id>/', drivedonation, name="profile"),
    
   
]