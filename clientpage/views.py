from django.shortcuts import render
from rest_framework.decorators import api_view
from clientpage.models import *
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.response import Response 
from clientpage.serializers import DriveSerializer
from clientpage.forms import * 
from django.contrib import messages

from geopy.distance import geodesic

# Create your views here.
def home(request):
    drive = DonationDrives.objects.all()
    context = {
        'drives': drive,
    }
    return render(request,'clientpage/home.html',context)


#detail view for drive donation
def drivedonation(request, id):
    drive = DonationDrives.objects.get(id=id)
    context = {
        "drive" : drive,
    }
    return render(request,'clientpage/profile.html',context)



@api_view(['POST'])
@permission_classes((AllowAny, ))
def locations(request,*args,**kwargs):
    print(request.data)
    lat = request.data['latitude']
    long = request.data['longitude']
    print(lat,long)
    origin = (lat,long)
    distance = {}
    for m in DonationDrives.objects.all():
        dest = (m.latitude, m.longitude)
        print(dest)
        distance[m.name] = round(geodesic(origin, dest).kilometers, 2)
    s_d = sorted(distance.items(), key=lambda x: x[1]) 
    context = []
    for i in range(len(s_d)):
        li = {}
        drivedata = DonationDrives.objects.get(name=s_d[i][0])
        serializer = DriveSerializer(drivedata, many=False)
        li.update({"driveinfo": serializer.data, "distance": s_d[i][1]})
        context.append(li)

    return Response({"message":"success", "data": context})

# @api_view(['GET'])
def covidposneg(request):
    return render(request,'clientpage/covidposneg.html')



def enquiryview(request,id):
    drive = DonationDrives.objects.get(id=id)
    context = {
        "drive" : drive,
    }
        
    return render(request,'clientpage/liveenquiry.html',context)

def appointmentview(request,id):
    drive = DonationDrives.objects.get(id=id)
    
    form = appointForm()
    context = {
        "drive" : drive,
        "form":form,
    }
    if request.method == "POST":
        print(request.POST)
        form = appointForm(request.POST)
        print(form.is_valid())
        if form.is_valid():
            appoint = form.save(commit=False)
            appoint.drive = drive
            appoint.save()
            messages.success(request,'Appointment success!')
            return render(request,'clientpage/profile.html',context)

    return render(request,'clientpage/appointment.html',context)
