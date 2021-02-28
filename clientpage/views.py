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
import tensorflow as tf 
from tensorflow.keras.optimizers import Adam
import numpy as np
import cv2
import os
from PIL import Image
        

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
        url = drivedata.get_absolute_url()
        serializer = DriveSerializer(drivedata, many=False)
        li.update({"driveinfo": serializer.data, "distance": s_d[i][1],'url': url})
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

INIT_LR = 1e-3
EPOCHS = 25
location = str(os.getcwd())+'\clientpage\model.h5'
print(location)
model = tf.keras.models.load_model(location)
opt = Adam(lr=INIT_LR, decay=INIT_LR / EPOCHS)
model.compile(loss="binary_crossentropy", optimizer=opt,
	metrics=["accuracy"])


def covid_detect(request):
    if request.method == "POST":
        print(request.POST)
        img = Image.open(request.FILES['image']).convert('RGB') 
        open_cv_image = np.array(img)
        image = open_cv_image[:, :, ::-1].copy()
        imageCpy = cv2.resize(image, (224, 224))

        images = [imageCpy]
        data =  np.stack(images, axis=0)

        print(data.shape)

        LABEL = ["covid-positive", "covid-negetive"]

        pred =  model.predict(data)
        label = LABEL[pred.argmax()]
        context={
            'pred': label,    
        }
        messages.success(request,'Inference Complete: '+ label + 'detected')
        return render(request,'clientpage/detectpage.html',context)
    return render(request,'clientpage/covid.html')