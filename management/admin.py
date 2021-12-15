from django.contrib import admin
from .models import Iran_adm1
from .models import Road, TollStation, Car

# Register your models here.

admin.site.register(Iran_adm1)
admin.site.register(Road)
admin.site.register(TollStation)
admin.site.register(Car)