from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request,'clientpage/home.html')


#detail view for drive donation
def drivedonation(request):
    return render(request,'clientpage/profile.html')

