from django.shortcuts import render,reverse
from django.contrib.auth.decorators import login_required
from clientpage.models import DonationDrives,Appointments
from django.http import HttpResponseRedirect
from django.contrib import messages

# Create your views here.
from organizers.forms import OrganizerForm

def complete(request):
    return render(request,'organizers/complete.html')

@login_required
def organizerform(request):
    if request.method =="POST":
        print(request.POST)
        print(request.FILES)
        form = OrganizerForm(request.POST,request.FILES)
        print(form.is_valid())
        if form.is_valid():
            organ = form.save(commit=False)
            organ.user = request.user
            organ.save()
            messages.success(request,'Form submission complete')
            return HttpResponseRedirect(reverse('dashboard'))
    return render(request, 'organizers/registerform.html')

@login_required
def dashboard(request):
    try:
        drive = DonationDrives.objects.get(user=request.user)  
    except:
        return HttpResponseRedirect(reverse('complete'))
    context = {
        'drive': drive,
    }

    return render(request, 'organizers/dashboard.html', context)

@login_required
def organapp(request, id):
    try:
        drive = DonationDrives.objects.get(user=request.user)  
    except:
        return reverse('complete')
    app = Appointments.objects.filter(drive=drive)
    context = {
        "appointments": app,
    }
    return render(request,'organizers/allappoints.html', context)