from rest_framework import serializers

from clientpage.models import * 


class DriveSerializer(serializers.ModelSerializer):
    class Meta:
        model = DonationDrives
        fields = '__all__'

