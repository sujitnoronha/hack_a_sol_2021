from django import forms 
from clientpage.models import *
from django.forms.widgets import DateTimeInput

class appointForm(forms.ModelForm):
    datetime = forms.DateTimeField(
        input_formats = ['%Y-%m-%dT%H:%M'],
        widget = forms.DateTimeInput(
            attrs={
                'type': 'datetime-local',
                'class': 'form-control'},
            format='%Y-%m-%dT%H:%M')
    )
    class Meta:
        model = Appointments
        fields = ['name', 'phonenumber', 'datetime', 'message']
         