from datetime import date

from .models import Road, TollStation, Iran_adm1, Car, AllNodes
from django.contrib.gis.db.models.functions import Distance, LineLocatePoint, Intersection
from django.db.models import F, Q


def small_car_location(name, id, range):
    city = Iran_adm1.objects.get(name=name)
    t1 = TollStation.objects.get(id=id)
    qs = AllNodes.objects.annotate(dist=Distance('location',t1.location)).filter(
        location__contained=city.geom,dist__lt=range,car__type='small')
    return qs

def street_width_violation():
    report_list = []
    locations = []
    narrow_roads = Road.objects.filter(width__lt=20)
    qs = AllNodes.objects.filter(id=0)
    for road in narrow_roads:
        qs = AllNodes.objects.annotate(dist=Distance('location',road.geom)).filter(dist=0,car__type='big')
        if qs.exists():
            for q in qs:
                locations.append(q.location)
                locations = list(dict.fromkeys(locations))
            # report_list.append({'road':road.name, 'car': qs.values('car')})
    # print(qs)
    # return qs
    return AllNodes.objects.filter(location__in=locations,car__type='big').distinct('car')

def car_toll_value(car=0, start="2021-06-08T04:53:47.7Z", end="2021-06-09T11:43:03.279847Z"):
    toll_paid = 0
    cars_loc = [[] for i in range(TollStation.objects.count())]
    roads_with_tollStation = []
    tollStations = TollStation.objects.all()
    tollStations_loc = []
    for i in range(TollStation.objects.count()):
        qs = Road.objects.annotate(
            dist=Distance('geom',tollStations[i].location)).filter(dist__lt=F('width'))
        roads_with_tollStation.append(qs)
        l = []
        for q in qs:
            x = Road.objects.filter(id=1).annotate(loc=LineLocatePoint(q.geom[0], tollStations[i].location)).values('loc')
            l.append(x[0]['loc'])
        tollStations_loc.append(l)
        print(qs,'\n')
    print(tollStations,'\n',tollStations_loc,'\n')
    #tollSatations
    for i, qs in enumerate(roads_with_tollStation):
        #roads
        for j, q in enumerate(qs):
            cars = AllNodes.objects.annotate(loc=LineLocatePoint(q.geom[0],'location'),dist=Distance('location',q.geom)).filter(
                car=car,date__gte=start,date__lte=end,dist__lt=q.width).order_by('date')
            cars_loc[i].append(cars.values('loc'))
            print(cars_loc[i])
            previous_loc = 1
            if cars_loc[i][j].exists():
                if tollStations_loc[i][j] - cars_loc[i][j][0]['loc'] < 0:
                    previous_loc = -1
                for k in range(len(cars_loc[i][j])):
                    current_loc = 1
                    if (tollStations_loc[i][j] - cars_loc[i][j][k]['loc']) < 0:
                        current_loc = -1
                    if current_loc*previous_loc == -1:
                        toll_paid += tollStations[i].toll_per_cross
                        if cars[0].car.type == 'big':
                            toll_paid += cars[0].car.load_volume*300
                    previous_loc = current_loc
        
    print(cars_loc,'\ntoll must be paid: ',toll_paid)
    return toll_paid