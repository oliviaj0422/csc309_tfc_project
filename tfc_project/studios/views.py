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


# Create your views here.

def set_distance(lon: float, lat: float):
    def inner(obj, lon=lon, lat=lat):
        _lon, _lat = obj.geolocation.strip().split(',')
        _lon, _lat = float(_lon), float(_lat)
        setattr(obj, '_distance', haversine((lat, lon), (_lat, _lon), unit=Unit.METERS))
        return obj

    return inner


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
                'Error': 'Nothing matched. Please check your input.'
            }
            return Response(resp)
        resp = {
            'Result': result[((page - 1) * 5):(page * 5)]
        }
        return Response(resp)