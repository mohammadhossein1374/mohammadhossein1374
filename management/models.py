from os import name
from django.contrib.gis.db import models
from django.db.models import constraints
from django.db.models import Q
from django.contrib.gis.geos import GEOSGeometry
from django.conf import settings
from . import validator
from django.core.exceptions import ValidationError


class Iran_adm1(models.Model):
    shape_leng = models.FloatField()
    shape_area = models.FloatField()
    adm1_en = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    adm1_pcode = models.CharField(max_length=50)
    adm1_ref = models.CharField(max_length=50, null=True)
    adm1alt1en = models.CharField(max_length=50, null=True)
    adm1alt2en = models.CharField(max_length=50, null=True)
    adm1alt1fa = models.CharField(max_length=50, null=True)
    adm1alt2fa = models.CharField(max_length=50, null=True)
    adm0_en = models.CharField(max_length=50)
    adm0_fa = models.CharField(max_length=50)
    adm0_pcode = models.CharField(max_length=50)
    date = models.DateField()
    validon = models.DateField()
    validto = models.DateField(null=True)
    geom = models.MultiPolygonField(srid=4326)

    def __str__(self) -> str:
        return self.name

class Road(models.Model):
    name = models.CharField(null=True, max_length=50)
    width = models.FloatField()
    geom = models.MultiLineStringField()

    def __str__(self) -> str:
        return self.name

class TollStation(models.Model):
    name = models.CharField(unique=True, max_length=100)
    toll_per_cross = models.FloatField()
    location = models.PointField()

    def __str__(self) -> str:
        return self.name

class Car(models.Model):
    type = models.CharField(choices=[('small','Small'), ('big','Big')],max_length=10)
    color = models.CharField(max_length=15)
    length = models.FloatField(validators=[validator.validate_length])
    load_volume = models.FloatField(null=True, 
        validators=[validator.validate_load_volume])
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,related_name='cars',
        on_delete=models.CASCADE,null=True
    )

    class Meta:
        constraints = [
            constraints.CheckConstraint(
                check=((Q(type='small') & Q(load_volume=None)) | Q(type='big') & ~Q(load_volume=None)),
                name='Check when type is small, load_volume be null'
            )
        ]

    def __str__(self) -> str:
        return  self.type + " " + self.color + " car ownd by " + str(self.owner)
class AllNodes(models.Model):
    car = models.ForeignKey(Car, related_name='locations', on_delete=models.CASCADE, null=True)
    location = models.PointField()
    date = models.DateTimeField()