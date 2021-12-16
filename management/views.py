from user.models import User
from rest_framework import pagination, serializers, status
from rest_framework import renderers
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import permissions
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from django.shortcuts import get_object_or_404, redirect
from rest_framework import mixins
from .serializers import CarSerializer, CarFilterSerializer, NodeSerializer
from .models import AllNodes, Car
from django import views
from django.shortcuts import render
from . import measurments
from .pagination import CarsPagination


class CarView(generics.ListAPIView):
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    template_name = 'car_view.html'
    serializer_class = CarSerializer
    pagination_class = CarsPagination

    def get_queryset(self):
        length = 'length'
        colorlist = self.request.query_params.get('color')
        color = None
        if colorlist:
            color = colorlist.split(',')
        age = self.request.query_params.get('age')
        if color and age:
            qs = Car.objects.filter(color__in=color, owner__age__gt=age)
        elif color:
            qs = Car.objects.filter(color__in=color)
        elif age:
            qs = Car.objects.filter(owner__age__gt=age)
        else:
            qs = Car.objects.all()
        
        return qs

    def get(self, request, *args, **kwargs):
        cars = self.get_serializer(self.get_queryset(), many=True)
        if request.accepted_renderer.format == 'html':
            serializer = CarFilterSerializer()
            context = {"serializer":serializer, 'cars': self.get_queryset()}
            return Response(status=status.HTTP_200_OK, data=context)
        return Response(status=status.HTTP_200_OK,data=cars.data)
    

class CarCreate(generics.GenericAPIView):
    serializer_class = CarSerializer
    permission_classes = [permissions.IsAdminUser]
    
    def get(self, request, *args, **kwargs):
        return Response(status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = CarSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        owner_id = serializer.validated_data.get('owner').get('national_code')
        owner = User.objects.filter(national_code=owner_id)
        if owner.exists():
            print('\n\n', serializer.validated_data, '\n\n', owner[0], '\n\n')
            serializer.save(owner=owner[0])
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

class CarViewSomeInfo(generics.ListAPIView):

    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    template_name = 'cars_list.html'

    serializer_class = NodeSerializer
    pagination_class = CarsPagination

    def get(self, request, *args, **kwargs):
        locations = self.get_serializer(self.get_queryset(), many=True)
        if request.accepted_renderer.format == 'html':
            serializer = CarFilterSerializer()
            context = {"serializer":serializer, 'locations': self.get_queryset()}
            return Response(status=status.HTTP_200_OK, data=context)
        return Response(status=status.HTTP_200_OK,data=locations.data)

    def get_queryset(self):
        city_name = self.request.query_params.get('city')
        tollStation_id = self.request.query_params.get('tollstation')
        range_around_city = self.request.query_params.get('range')
        street_width_violation = self.request.query_params.get('violation')
        if city_name and range_around_city and tollStation_id:
            qs = measurments.small_car_location(city_name, tollStation_id, range_around_city)
        elif street_width_violation == '1':
            qs = measurments.street_width_violation()
        else:
            qs = AllNodes.objects.filter(id=0)
        return qs