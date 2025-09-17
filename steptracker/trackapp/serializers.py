from rest_framework import serializers
from django.contrib.auth.models import User
from .models import StepRecord

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "password")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class StepRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = StepRecord
        fields = ("date", "steps")
