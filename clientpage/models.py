from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class DonationDrives(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=True, null=True)
    latitude = models.DecimalField(max_digits=22, decimal_places=16, blank=True, null=True)
    longitude = models.DecimalField(max_digits=22, decimal_places=16, blank=True, null=True)
    timeopen = models.TimeField(auto_now=False)
    timeclose = models.TimeField(auto_now=False)
    address = models.CharField(max_length=300, blank=True, null=True)
    description = models.CharField(max_length=300, blank=True, null=True)

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse("profile", kwargs={"pk": self.pk})
    
