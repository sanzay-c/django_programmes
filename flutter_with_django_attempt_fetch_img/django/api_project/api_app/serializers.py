# myapp/serializers.py

from rest_framework import serializers
from .models import PersonDetail
from django.conf import settings
from django.db.models import ImageField

class PersonDetailSerializer(serializers.ModelSerializer):
    # This method will return the full URL of the profile picture
    profile_pic = serializers.SerializerMethodField()

    class Meta:
        model = PersonDetail
        # fields = ['id', 'name', 'profile_pic']
        fields = '__all__'

    def get_profile_pic(self, obj):
        if obj.profile_pic:
            # Build the full URL
            return settings.BASE_URL + obj.profile_pic.url
        return None
