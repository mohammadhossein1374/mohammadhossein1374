from django.contrib.gis.geos.geometry import GEOSGeometry
from rest_framework import serializers, status
from rest_framework import renderers
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from .serializers import GetOwnerSerializer, PostOwnerSerializer
from .models import User
from .pagination import OwnerPagination


class OwnerView(generics.ListCreateAPIView):

    queryset = User.objects.all()
    pagination_class = OwnerPagination
    serializer_class = GetOwnerSerializer

    def get_serializer_class(self, *args, **kwargs):
        if self.request.method in ['POST', 'PUT', 'PATCH']:
            return PostOwnerSerializer
        elif self.request.method in ['GET', 'HEAD']:
            return GetOwnerSerializer
    def perform_create(self, serializer):
        serializer.create(serializer.validated_data)