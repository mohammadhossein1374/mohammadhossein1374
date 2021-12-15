from os import read
from django.db.models import fields
from rest_framework import serializers
from .models import Car, AllNodes
from user.models import User

from management import models

class OwnerModelSerializer(serializers.Serializer):
    national_code = serializers.IntegerField(min_value=10000, max_value=10 ** 10)
    age = serializers.IntegerField(min_value=18)


class CarSerializer(serializers.ModelSerializer):
    owner = OwnerModelSerializer()
    class Meta:
        model = Car
        fields = ['type', 'color', 'length', 'load_volume', 'owner']

class NodeSerializer(serializers.ModelSerializer):
    car = CarSerializer()
    class Meta:
        model = AllNodes
        fields = ['location', 'car']

class CarFilterSerializer(serializers.Serializer):
    color = serializers.CharField()
    age = serializers.CharField()