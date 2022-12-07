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

from studios.models import Studio


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
    pagination_class = PageNumberPagination
    serializer_class = ClassInstanceSerializer

    def get_queryset(self):
        studio = Studio.objects.filter(name=self.kwargs['studio']).first()
        
        current_time = timezone.now()
        classes = ClassInstance.objects.filter(the_class__studio=studio,start_time__gte=current_time,is_cancelled=False).order_by('start_time')
        
        return classes

        


class UserEnrolClass(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        
        class_id = self.kwargs['class_id']
        current_time = timezone.now().date()
        class_instance = get_object_or_404(ClassInstance, id=class_id)
        user_class = UserEnrolledClass.objects.filter(class_instance=class_instance)
        if current_time <= request.user.sub_edate:
            if not user_class:
                if class_instance.start_time.date() >= current_time and class_instance.space_availability > 0:
                    class_instance.space_availability -= 1
                    class_instance.save()
                    UserEnrolledClass.objects.create(user_id=request.user.id,
                                                    class_instance=class_instance,
                                                    class_instance_name=class_instance.the_class.name,
                                                    class_instance_start_time=class_instance.start_time,
                                                    class_instance_end_time=class_instance.end_time)
                    return JsonResponse({'detail': 'successfully enrolled'})
                else:
                    return JsonResponse({
                        'detail': 'enrolment failed because of start time and/or space availability'})
            else:
                return JsonResponse({'detail': 'Enrolment failed since the user has enrolled this class instance'})
        else:
            return JsonResponse({
                'detail': 'Enrolment failed since the user is not '
                           'subscribed'})

class UserEnrolAllFutureClasses(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        class_id = self.kwargs['class_id']
        current_time = timezone.now().date()
        the_class_instance = ClassInstance.objects.filter(id=class_id).first()
        if current_time <= request.user.sub_edate:
            if the_class_instance:
                the_class = the_class_instance.the_class
                class_instances_needed = ClassInstance.objects.filter(the_class=the_class, is_cancelled=False)
                flag = False
                for class_instance in class_instances_needed:
                    user_class = UserEnrolledClass.objects.filter(class_instance=class_instance)
                    if class_instance.start_time.date() >= current_time and class_instance.space_availability > 0 and (not user_class):
                        flag = True
                        class_instance.space_availability -= 1
                        class_instance.save()
                        UserEnrolledClass.objects.create(user_id=request.user.id,
                                                        class_instance=class_instance,
                                                        class_instance_name=class_instance.the_class.name,
                                                        class_instance_start_time=class_instance.start_time,
                                                        class_instance_end_time=class_instance.end_time)
                if flag:
                    return JsonResponse({'detail': 'successfully enrolled'})
                else:
                    return JsonResponse({'detail':'Enrolment failed since no required class instances are found'})
            else:
                return JsonResponse({'detail': 'Enrolment failed since no required class instances are found'})
        else:
            return JsonResponse({
                'detail': 'Enrolment failed since the user is not '
                           'subscribed'})



class UserDeleteClass(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        current_time = timezone.now().date()
        if current_time <= request.user.sub_edate:
            class_id = self.kwargs['class_id']
            current_time = timezone.now()
            class_instance = get_object_or_404(ClassInstance, id=class_id)
            user_class_instance = get_object_or_404(UserEnrolledClass,
                                                    class_instance=class_instance,
                                                    user_id=request.user.id)
            if class_instance.start_time > current_time:
                user_class_instance.delete()
                class_instance.space_availability += 1
                class_instance.save()
                return JsonResponse({'detail': 'successfully dropped'})
            else:
                return JsonResponse({'detail': 'Dropping the class failed'})
        else:
            return JsonResponse({
                'detail': 'Dropping the class failed since the user is not '
                           'subscribed'})

class DropAllFutureClasses(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        class_id = self.kwargs['class_id']
        current_time = timezone.now().date()
        the_class_instance = ClassInstance.objects.filter(id=class_id).first()
        if current_time <= request.user.sub_edate:
            if the_class_instance:
                the_class = the_class_instance.the_class
                class_instances_needed = ClassInstance.objects.filter(the_class=the_class, is_cancelled=False)
                flag = False
                t = timezone.now()
                for class_instance in class_instances_needed:
                    user_class_instance = UserEnrolledClass.objects.filter(class_instance=class_instance,user_id=request.user.id).first()
                    if class_instance.start_time > t and user_class_instance:
                        user_class_instance.delete()
                        class_instance.space_availability += 1
                        class_instance.save()
                        flag  =True 
                if flag:
                    return JsonResponse({'detail': 'successfully dropped'})
                else:
                    return JsonResponse({'detail':'Dropping classes failed since no required class instances are found'})
            else:
                return JsonResponse({'detail': 'Dropping classes failed since no required class instances are found'})
        else:
            return JsonResponse({
                'detail': 'Dropping classes failed since the user is not '
                           'subscribed'})

class MyClassHistory(ListAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination
    serializer_class = UserEnrolledClassSerializer

    def get_queryset(self):
        enrolled_pairs = UserEnrolledClass.objects.filter(user_id=self.request.user.id).order_by('class_instance__start_time')
        return enrolled_pairs

class MyClassSchedule(ListAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination
    serializer_class = UserEnrolledClassSerializer

    def get_queryset(self):
        enrolled_pairs = UserEnrolledClass.objects.filter(user_id=self.request.user.id,class_instance__is_cancelled=False).order_by('class_instance__start_time')

        return enrolled_pairs


class SearchOrFilterByClassNameView(ListAPIView):
    pagination_class = PageNumberPagination
    serializer_class = ClassInstanceSerializer

    def get_queryset(self):
        studio = Studio.objects.get(name=self.kwargs['studio'])
        the_class = ClassInstance.objects.filter(the_class__studio=studio,the_class__name=self.kwargs['class'],is_cancelled=False)

        return the_class



class SearchOrFilterByCoachView(ListAPIView):
    pagination_class = PageNumberPagination
    serializer_class = ClassInstanceSerializer

    def get_queryset(self):
        studio = Studio.objects.get(name=self.kwargs['studio'])
        the_class = ClassInstance.objects.filter(the_class__studio=studio,the_class__coach=self.kwargs['coach'],is_cancelled=False)
        return the_class



class SearchOrFilterByDateView(ListAPIView):
    pagination_class = PageNumberPagination
    serializer_class = ClassInstanceSerializer

    def get_queryset(self):
        studio = Studio.objects.get(name=self.kwargs['studio'])
        the_class = ClassInstance.objects.filter(the_class__studio=studio,start_time__year=self.kwargs['year'],start_time__month=self.kwargs['month'],start_time__day=self.kwargs['day'],is_cancelled=False)

        return the_class




class SearchOrFilterByTimeRangeView(APIView):
    def get(self, request, *args, **kwargs):
        hour1 = kwargs['hour1']
        minute1 = kwargs['minute1']
        hour2 = kwargs['hour2']
        minute2 = kwargs['minute2']
        t1 = datetime.time(hour1, minute1, 0)
        t2 = datetime.time(hour2, minute2, 0)
        studio = Studio.objects.get(name=self.kwargs['studio'])
        class_instances = ClassInstance.objects.filter(the_class__studio=studio)
        if class_instances:
            
            result = []
            for c in class_instances:
                if c.start_time.time() >= t1 and c.end_time.time()<=t2:
                    result.append( f'{c.the_class.name} with id{c.id} (from {c.start_time} to {c.end_time})')                   
            if result:
                result1 = {'detail': result}
                return JsonResponse(result1)
            else:
                return JsonResponse({'detail': []})
        else:
            return JsonResponse({'detail': []})
