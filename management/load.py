from pathlib import Path
from django.contrib.gis.utils import LayerMapping
from .models import Iran_adm1
from .models import Road, TollStation, Car, AllNodes
from user.models import User
import json
import re
from django.contrib.gis.geos import GEOSGeometry


# Auto-generated `LayerMapping` dictionary for Iran_adm1 model
iran_adm1_mapping = {
    'shape_leng': 'Shape_Leng',
    'shape_area': 'Shape_Area',
    'adm1_en': 'ADM1_EN',
    'name': 'ADM1_FA',
    'adm1_pcode': 'ADM1_PCODE',
    'adm1_ref': 'ADM1_REF',
    'adm1alt1en': 'ADM1ALT1EN',
    'adm1alt2en': 'ADM1ALT2EN',
    'adm1alt1fa': 'ADM1ALT1FA',
    'adm1alt2fa': 'ADM1ALT2FA',
    'adm0_en': 'ADM0_EN',
    'adm0_fa': 'ADM0_FA',
    'adm0_pcode': 'ADM0_PCODE',
    'date': 'date',
    'validon': 'validOn',
    'validto': 'validTo',
    'geom': 'MULTIPOLYGON',
}


world_shp = Path(__file__).resolve().parent.parent / 'TM_WORLD_BORDERS-0.3' / 'TM_WORLD_BORDERS-0.3.shp'
iran_admallp_shp = Path(__file__).resolve().parent.parent / 'iran-data' / 'irn_adm_unhcr_20190514_shp' / 'irn_admbndp_admALL_unhcr_itos_20190514.shp'
iran_admalll_shp = Path(__file__).resolve().parent.parent / 'iran-data' / 'irn_adm_unhcr_20190514_shp' / 'irn_admbndl_admALL_unhcr_itos_20190514.shp'
iran_adm1_shp = Path(__file__).resolve().parent.parent / 'iran-data' / 'irn_adm_unhcr_20190514_shp' / 'irn_admbnda_adm1_unhcr_20190514.shp'
DATA_DIR = Path(__file__).resolve().parent.parent / 'data'

def run_iran_adm1(verbose=True):
    lm = LayerMapping(Iran_adm1, iran_adm1_shp, iran_adm1_mapping, transform=False)
    lm.save(strict=True, verbose=verbose)

def road_data():
    # Opening JSON file
    with open(DATA_DIR / 'roads.json', 'r') as openfile:
    
        # Reading from json file
        json_object = json.load(openfile)
    
    for obj in json_object:
        name = obj.get('name')
        width = obj.get('width')
        geom = obj.get('geom').split(';')
        srid = geom[0].split('=')[1]
        linestrings = geom[1]
        # text = obj.get('geom').split(';')[1]
        # linestrings = re.findall("\d+[.]\d+\s{1}\d+[.]{1}\d+",text)
        road = Road.objects.create(name=name, width=width,
         geom=GEOSGeometry(linestrings,srid=srid))
        road.save()

def tollStations_data():
    with open(DATA_DIR / 'tollStations.json', 'r') as openfile:
        json_object = json.load(openfile)
    
    for obj in json_object:
        name = obj.get('name')
        toll_per_cross = obj.get('toll_per_cross')
        location = obj.get('location').split(';')
        srid = location[0].split('=')[1]
        point = location[1]
        tollStation = TollStation.objects.create(
            name=name, toll_per_cross=toll_per_cross, location=GEOSGeometry(
                point, srid=srid
            )
        )
        tollStation.save()

def owners_data():
    with open(DATA_DIR / 'owners.json', 'r') as openfile:
        json_object = json.load(openfile)
    
    for obj in json_object:
        name = obj.get('name')
        national_code = obj.get('national_code')
        age = obj.get('age')
        total_toll_paid = obj.get('total_toll_paid')
        ownerCar = obj.get('ownerCar')
        owner = User.objects.create(
            name=name, national_code=national_code, age=age,
            total_toll_paid=total_toll_paid, password='00000000'
        )
        owner.save()
        for car in ownerCar:
            id = car.get('id')
            type = car.get('type')
            color = car.get('color')
            length = car.get('length')
            load_volume = car.get('load_volume')
            c = Car.objects.create(id=id, type=type, color=color,
                length=length, load_volume=load_volume
            )
            c.save()
            owner.cars.add(c)

def all_nodes():
    with open(DATA_DIR / 'all_nodes.json', 'r') as openfile:
        json_object = json.load(openfile)
    
    for obj in json_object:
        car = Car.objects.get(id=obj.get('car'))
        location = obj.get('location').split(';')
        srid = location[0].split('=')[1]
        point = location[1]
        date = obj.get('date')
        node = AllNodes.objects.create(
            car=car, location=GEOSGeometry(point,srid=srid), date=date)
        node.save()

def run_all():
    run_iran_adm1()
    road_data()
    tollStations_data()
    owners_data()
    all_nodes()