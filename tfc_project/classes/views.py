from datetime import datetime, timedelta
import datetime
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import render

# Create your views here.
from django.utils import timezone
from rest_framework.generics import ListAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
import django
from rest_framework.views import APIView

from classes.models import Class, ClassInstance

from classes.models import UserEnrolledClass

from classes.serializers import ClassInstanceSerializer,UserEnrolledClassSerializer


def get_weekday(x):
    if x == 1:
        return 'Monday'
    if x == 2:
        return 'Tuesday'
    if x == 3:
        return 'Wednesday'
    if x == 4:
        return 'Thursday'
    if x == 5:
        return 'Friday'
    if x == 6:
        return 'Saturday'
    if x == 7:
        return 'Sunday'


class ShowClassInStudioView(ListAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination
    serializer_class = ClassInstanceSerializer

    def get_queryset(self):
        studio = self.kwargs['studio']
        current_time = timezone.now()
        classes = ClassInstance.objects.filter(the_class__studio=studio,start_time__gte=current_time,is_cancelled=False).order_by('start_time')
        if classes:
            return classes
        else:
            raise Http404


class UserEnrolClass(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        class_id = request.POST.get('class_id', '')
        current_time = timezone.now()
        class_instance = get_object_or_404(ClassInstance, id=class_id)
        #if request.user.is_subscribed:
        if class_instance.start_time >= current_time and class_instance.space_availability > 0:
            class_instance.space_availability -= 1
            class_instance.save()
            UserEnrolledClass.objects.create(user_id=request.user.id,
                                             class_instance=class_instance,
                                             class_instance_name=class_instance.the_class.name,
                                             class_instance_start_time=class_instance.start_time,
                                             class_instance_end_time=class_instance.end_time)
            return Response({'details': 'successfully enrolled'})
        else:
            return Response({
                'details': 'enrolment failed because of start time and/or space availability'})
        # else:
        #     Response({
        #                  'details': 'enrolment failed since the user is not '
        #                             'subscribed'})


class UserDeleteClass(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        #if request.user.is_subscribed:
            class_id = request.POST.get('class_id', '')
            current_time = timezone.now()
            class_instance = get_object_or_404(ClassInstance, id=class_id)
            user_class_instance = get_object_or_404(UserEnrolledClass,
                                                    class_instance=class_instance,
                                                    user_id=request.user.id)
            if class_instance.start_time > current_time:
                user_class_instance.delete()
                class_instance.space_availability += 1
                class_instance.save()
                return Response({'details': 'successfully deleted'})
            else:
                return Response({'details': 'deletion failed'})
        # else:
        #     Response({
        #         'details': 'Dropping class failed since the user is not '
        #                    'subscribed'})

class MyClassHistory(ListAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination
    serializer_class = UserEnrolledClassSerializer

    def get_queryset(self):
        enrolled_pairs = UserEnrolledClass.objects.filter(user_id=self.request.user.id).order_by('class_instance__start_time')
        if enrolled_pairs:
            return enrolled_pairs
        else:
            raise Http404

class MyClassSchedule(ListAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination
    serializer_class = UserEnrolledClassSerializer

    def get_queryset(self):
        enrolled_pairs = UserEnrolledClass.objects.filter(user_id=self.request.user.id,class_instance__is_cancelled=False).order_by('class_instance__start_time')
        if enrolled_pairs:
            return enrolled_pairs
        else:
            raise Http404


class SearchOrFilterByClassNameView(ListAPIView):
    pagination_class = PageNumberPagination
    serializer_class = ClassInstanceSerializer

    def get_queryset(self):
        the_class = ClassInstance.objects.filter(the_class__studio=self.kwargs['studio'],the_class__name=self.kwargs['class'],is_cancelled=False)
        if the_class:
            return the_class
        else:
            raise Http404


class SearchOrFilterByCoachView(ListAPIView):
    pagination_class = PageNumberPagination
    serializer_class = ClassInstanceSerializer

    def get_queryset(self):
        the_class = ClassInstance.objects.filter(the_class__studio=self.kwargs['studio'],the_class__coach=self.kwargs['coach'],is_cancelled=False)
        if the_class:
            return the_class
        else:
            raise Http404


class SearchOrFilterByDateView(ListAPIView):
    pagination_class = PageNumberPagination
    serializer_class = ClassInstanceSerializer

    def get_queryset(self):
        the_class = ClassInstance.objects.filter(the_class__studio=self.kwargs['studio'],start_time__year=self.kwargs['year'],start_time__month=self.kwargs['month'],start_time__day=self.kwargs['day'],is_cancelled=False)
        if the_class:
            return the_class
        else:
            raise Http404


class SearchOrFilterByTimeRangeView(APIView):
    def get(self, request, *args, **kwargs):
        hour1 = kwargs['hour1']
        minute1 = kwargs['minute1']
        hour2 = kwargs['hour2']
        minute2 = kwargs['minute2']
        t1 = datetime.time(hour1, minute1, 0)
        t2 = datetime.time(hour2, minute2, 0)
        class_instances = ClassInstance.objects.filter(the_class__studio=kwargs['studio'])
        if class_instances:
            i = 1
            result = {}
            for c in class_instances:
                if c.start_time.time() >= t1 and c.end_time.time()<=t2:
                    result[i] = f'{c.the_class.name} with id{c.id}'
                    i += 1
            if result:
                return Response(result)
            else:
                raise Http404
        else:
            raise Http404
