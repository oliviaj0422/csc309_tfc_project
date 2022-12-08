from collections import OrderedDict

from django.forms import model_to_dict
from django.http.request import HttpRequest
from django.http.response import JsonResponse, Http404
from geopy.distance import geodesic
from haversine import haversine, Unit
from rest_framework.response import Response
from rest_framework.views import APIView

from classes.models import Class
from .models import Studio

from classes.models import ClassInstance
import math
from math import pi

# lat lon - > distance
# 计算经纬度之间的距离，单位为千米

EARTH_REDIUS = 6378.137


def rad(d):
	return d * pi / 180.0


def getDistance(lat1, lng1, lat2, lng2):
	radLat1 = rad(lat1)
	radLat2 = rad(lat2)
	a = radLat1 - radLat2
	b = rad(lng1) - rad(lng2)
	s = 2 * math.asin(
		math.sqrt(math.pow(math.sin(a / 2), 2) + math.cos(radLat1) * math.cos(radLat2) * math.pow(math.sin(b / 2), 2)))
	s = s * EARTH_REDIUS
	return s

class DistanceClass(APIView):
    def get(self, request, *args, **kwargs):
        print(request.GET)
        x1 = float(request.GET.get('x1', '0'))
        y1 = float(request.GET.get('y1', '0'))
        x2 = float(request.GET.get('x2', '0'))
        y2 = float(request.GET.get('y2', '0'))
        
        return Response({'details': getDistance(x1,y1,x2,y2)})


# Create your views here.

def set_distance(lon: float, lat: float):
    def inner(obj, lon=lon, lat=lat):
        _lon, _lat = obj.geolocation.strip().split(',')
        _lon, _lat = float(_lon), float(_lat)
        setattr(obj, '_distance', haversine((lat, lon), (_lat, _lon), unit=Unit.METERS))
        return obj

    return inner


class ShowClassInStudioView(APIView):
    def get(self, request, *args, **kwargs):
        studio_name = request.GET.get('name', None)
        if studio_name:
            studio = Studio.objects.filter(name=studio_name).first()
            classes_model = ClassInstance.objects.filter(the_class__studio=studio)
            classes = []
            for item in classes_model:
                classes.append({"classname":item.class_name,
                                "id":item.id,
                                "description":item.description,
                                "coach":item.coach,
                                "keywords":item.keywords,
                                "spaceavailability":item.space_availability,
                                "starttime":item.start_time,
                                "endtime":item.end_time,
                                })
            # classes = ClassInstance.objects.filter(the_class__studio=cls_id,start_time__gte=current_time,is_cancelled=False).order_by('start_time')
        else:
            classes = []
            for item in ClassInstance.objects.all():
                classes.append({"classname":item.class_name,
                                "id":item.id,
                                "description":item.description,
                                "coach":item.coach,
                                "keywords":item.keywords,
                                "spaceavailability":item.space_availability,
                                "starttime":item.start_time,
                                "endtime":item.end_time,
                                })
        if classes:
            resp = {
            'data':classes
            }
            print(resp)
            return  Response(resp)
        else:
            print(2)
            return Response({'details': 'Not found'})
        

class DistanceView(APIView):
    def get(self, request, *args, **kwargs):
        lon, lat, page = request.GET.get('lon'), request.GET.get('lat'), request.GET.get('page')
        lon, lat, page = float(lon), float(lat), int(page)
        studios = Studio.objects.all()
        studios = list(map(set_distance(lon, lat), studios))
        studios.sort(key=lambda o: getattr(o, '_distance'))
        result = list(map(dict, studios))[((page - 1) * 5):(page * 5)]
        for item in result:
            _lon, _lat = float((item['geolocation'].split(","))[0]), float((item['geolocation'].split(","))[1])
            item['distance'] = (haversine((lat, lon), (_lat, _lon)))

        resp = {
            'data':result
        }
        return Response(resp)


class StudioView(APIView):
    def get(self, request, *args, **kwargs):
        result = []
        """Check method. GET only"""
        if request.method == 'GET':
            key, page,lon,lat = request.GET.get('key'), int(request.GET.get('page')),float(request.GET.get('lon')), float(request.GET.get('lat'))
        else:
            resp = {
                'Error': 'GET method only.'
            }
            return Response(resp)
        """Search by studio name"""
        namestudios = Studio.objects.filter(name__contains=key).values()
        if len(namestudios) > 0:
            for item in namestudios:
                result.append(item)
        """Search by studio address"""
        addressstudios = Studio.objects.filter(address__contains=key).values()
        if len(addressstudios) > 0:
            for item in addressstudios:
                result.append(item)
        """Search by postal code, percisely"""
        postalcode = Studio.objects.filter(postalcode=key).values()
        if len(postalcode) > 0:
            for item in postalcode:
                result.append(item)
        """Search by phone number, percisely"""
        phonenumber = Studio.objects.filter(phonenumber=key).values()
        if len(phonenumber) > 0:
            for item in phonenumber:
                result.append(item)
        """Search by amenity type"""
        amenitiestype = Studio.objects.filter(amenitiestype__contains=key).values()
        if len(amenitiestype) > 0:
            for item in amenitiestype:
                result.append(item)
        """Search by class name"""
        nameclasslist = Class.objects.filter(name__contains=key)
        if len(nameclasslist) > 0:
            for item in nameclasslist:
                result.append(model_to_dict(item.studio))
        """Search by coach name, percisely"""
        coathclasslist = Class.objects.filter(coach=key)
        if len(coathclasslist) > 0:
            for item in coathclasslist:
                result.append(model_to_dict(item.studio))
        newResult = []
        for item in result:
            if item not  in newResult:
                newResult.append(item)
        result = newResult
        for item in result:
            _lon, _lat = float((item['geolocation'].split(","))[0]), float((item['geolocation'].split(","))[1])
            item['distance'] = (haversine((lat, lon), (_lat, _lon)))
        result = sorted(result, key=lambda book: book['distance'])
        if len(result) == 0:
            resp = {
                'Result': []
            }
            return Response(resp)
        resp = {
            'Result': result[((page - 1) * 5):(page * 5)]
        }
        return Response(resp)