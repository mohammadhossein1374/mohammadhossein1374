from os import read
from django.core.exceptions import ValidationError
from rest_framework import serializers
from .models import User
from management.models import Car


class PostCarSerializer(serializers.ModelSerializer):
    # type = serializers.CharField(source='management.car.type')
    # color = serializers.CharField(allow_null=True, source='car.color')
    # length = serializers.IntegerField(allow_null=True, source='car.length')
    # load_volume = serializers.IntegerField(allow_null=True, source='car.load_volume')
    class Meta:
        model = Car
        fields = ['type', 'color', 'length', 'load_volume']

class PostOwnerSerializer(serializers.ModelSerializer):
    # cars = PostCarSerializer(allow_null=True)
    class Meta:
        model = User
        fields = ['name', 'national_code', 'age', 'total_toll_paid']
    
    def create(self, validated_data):
        # car = validated_data.pop('cars')
        owner = User.objects.create(**validated_data)
        owner.password = '00000000'
        owner.save()
        # if car:
        #     Car.objects.create(**car, owner=owner)
        #     owner.cars.add(car)
        #     owner.save()
        return owner


class GetOwnerSerializer(serializers.ModelSerializer):
    cars = serializers.StringRelatedField(many=True,read_only=True)
    class Meta:
        model = User
        fields = ['id','name', 'national_code', 'age', 'total_toll_paid', 'cars']
        read_only_fields = ['cars']
