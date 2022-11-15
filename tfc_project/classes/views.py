from datetime import datetime, timedelta

from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView

from classes.models import Class, ClassInstance


class CreateClassInstancesView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        the_class = get_object_or_404(Class, studio=kwargs['studio'],
                                      name=kwargs['class'])
        t1 = the_class.start_time
        t2 = the_class.end_time
        duration = the_class.duration
        i = t1
        count = 0
        while i < t2:
            ClassInstance.objects.create(name=the_class.name,
                                         description=the_class.description,
                                         coach=the_class.coach,
                                         keywords=the_class.keywords,
                                         capacity=the_class.capacity,
                                         space_availability=the_class.space_availability,
                                         start_time=i,
                                         duration=duration,
                                         studio=the_class.studio)
            i = i + timedelta(days=7)
            count += 1
        return Response({'the number of created class instances': count })

class ShowClassInStudioView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        class_instances = ClassInstance.objects.filter(studio=kwargs['studio'])

        current_time = timezone.now()
        lst = []
        for i in class_instances:
            if i.start_time >= current_time:
                lst.append(i)

        # sort by start time
        n = len(lst)
        for i in range(1, n):
            key = lst[i]
            j = i-1
            while (j>=0 and lst[j].start_time>key.start_time):
                lst[j+1] = lst[j]
                j = j-1
            lst[j+1] = key

        temp = []
        for i in lst:
            temp.append(i.get_class_info())
        return JsonResponse(temp, safe=False)


