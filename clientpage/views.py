from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view
from clientpage.models import *
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.response import Response 
from clientpage.serializers import DriveSerializer
from clientpage.forms import * 
from django.contrib import messages
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

from geopy.distance import geodesic

from webpush import send_user_notification

# Create your views here.
def home(request):
    webpush_settings = getattr(settings, 'WEBPUSH_SETTINGS', {})
    vapid_key = webpush_settings.get('VAPID_PUBLIC_KEY')
    user = request.user
    drive = DonationDrives.objects.all()
    context = {
        'drives': drive,
        user: user,
        'vapid_key': vapid_key
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
@csrf_exempt
def locations(request,*args,**kwargs):
    lat = request.data['latitude']
    long = request.data['longitude']
    user_id = request.data['id']
    user = get_object_or_404(User, pk=user_id)
    print(lat,long)
    origin = (lat,long)
    distance = {}
    for m in DonationDrives.objects.all():
        dest = (m.latitude, m.longitude)
        # CAN ADD THE FOLLOWS:
        # if round(geodesic(origin, dest).kilometers, 2) < 5:
        # adding this condition will shortlist only those hospitals which are within a 5 kms
        distance[m.name] = round(geodesic(origin, dest).kilometers, 2)
        # send notification starts from here
        head_data = m.name
        body_data = m.name + " is now available " + str(distance[m.name]) + " kms away from you"
        payload = {'head': head_data, 'body': body_data}
        send_user_notification(user=user, payload=payload, ttl=1000)
        # ends here

    s_d = sorted(distance.items(), key=lambda x: x[1]) 
    context = []
    for i in range(len(s_d)):
        li = {}
        drivedata = DonationDrives.objects.get(name=s_d[i][0])
        serializer = DriveSerializer(drivedata, many=False)
        li.update({"driveinfo": serializer.data, "distance": s_d[i][1]})
        context.append(li)

    return Response({"message":"success", "data": context})



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
