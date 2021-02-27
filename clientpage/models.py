from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse

# Create your models here.

class DonationDrives(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(blank=False, null=True, upload_to="donationprofiles")
    latitude = models.DecimalField(max_digits=22, decimal_places=16, blank=True, null=True)
    longitude = models.DecimalField(max_digits=22, decimal_places=16, blank=True, null=True)
    timeopen = models.TimeField(auto_now=False)
    timeclose = models.TimeField(auto_now=False)
    address = models.CharField(max_length=300, blank=True, null=True)
    description = models.CharField(max_length=300, blank=True, null=True)

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse("profile", kwargs={"id": self.pk})


class Appointments(models.Model):
    drive = models.ForeignKey(DonationDrives, related_name='drives', on_delete=models.CASCADE)
    name = models.CharField(max_length=200, blank=True, null=True)
    phonenumber = models.CharField(max_length=20, blank=True, null=True)
    datetime = models.DateField(auto_now=False, auto_now_add=False)
    message = models.CharField(max_length=100, blank=True, null=True)
    user = models.name = models.ForeignKey(User, related_name='user', on_delete=models.DO_NOTHING, null=True, blank=True)

    def __str__(self):
        return str(self.name)