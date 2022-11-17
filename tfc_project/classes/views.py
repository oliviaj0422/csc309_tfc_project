from datetime import datetime, timedelta
import datetime
from django.http import Http404, JsonResponse
from django.shortcuts import render

# Create your views here.
from django.utils import timezone
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView

from classes.models import Class, ClassInstance

from classes.models import UserEnrolledClass

def get_weekday(x):
    if x==1:
        return 'Monday'
    if x==2:
        return 'Tuesday'
    if x==3:
        return 'Wednesday'
    if x==4:
        return 'Thursday'
    if x==5:
        return 'Friday'
    if x==6:
        return 'Saturday'
    if x==7:
        return 'Sunday'

class ShowClassInStudioView(APIView):
    permission_classes = [IsAuthenticated]
    pagination_class = LimitOffsetPagination

    def get(self, request, *args, **kwargs):
        classes = Class.objects.filter(studio=kwargs['studio'])
        current_time = timezone.now()
        if classes:
            lst = []
            for the_class in classes:
                class_instances = ClassInstance.objects.filter(the_class=the_class)
                for i in class_instances:
                    if i.start_time >= current_time and i.is_cancelled == False:
                        lst.append(i)
            # sort by start time
            n = len(lst)
            for i in range(1, n):
                key = lst[i]
                j = i - 1
                while (j >= 0 and lst[j].start_time > key.start_time):
                    lst[j + 1] = lst[j]
                    j = j - 1
                lst[j + 1] = key

            temp = {}
            j = 1
            for i in lst:
                temp[j] = i.get_class_info()
                j += 1
            return Response(temp)
        else:
            raise Http404



class UserEnrolClass(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        class_id = request.POST.get('class_id', '')
        current_time = timezone.now()
        class_instance = get_object_or_404(ClassInstance, id=class_id)
        # if request.user.is_subscribed:
        if class_instance.start_time >= current_time and class_instance.space_availability > 0:
            class_instance.space_availability -= 1
            class_instance.save()
            UserEnrolledClass.objects.create(user_id=request.user.id,
                                             class_id=class_id)
            return Response({'details': 'successfully enrolled'})
        else:
            return Response({
                'details': 'enrolment failed because of start time and/or space availability'})
        # else:
        #     Response({'details': 'enrolment failed since the user is not subscribed'})


class UserDeleteClass(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        class_id = request.POST.get('class_id', '')
        current_time = timezone.now()
        user_class_instance = get_object_or_404(UserEnrolledClass, class_id=class_id, user_id=request.user.id)
        class_instance = get_object_or_404(ClassInstance, id=class_id)
        if class_instance.start_time > current_time:
            user_class_instance.delete()
            class_instance.space_availability += 1
            class_instance.save()
            return Response({'details': 'successfully deleted'})
        else:
            return Response({'details': 'deletion failed'})

class MyClassHistory(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        enrolled_pairs = UserEnrolledClass.objects.filter(
            user_id=request.user.id)

        lst = []
        for pair in enrolled_pairs:
            class_id = pair.class_id
            class_instance = ClassInstance.objects.get(id=class_id)
            lst.append(class_instance)

        n = len(lst)
        for i in range(1, n):
            key = lst[i]
            j = i - 1
            while (j >= 0 and lst[j].start_time > key.start_time):
                lst[j + 1] = lst[j]
                j = j - 1
            lst[j + 1] = key
        result = {}
        i = 1
        for class_instance in lst:
            result[i] = f'{class_instance.the_class.name} with id{class_instance.id} in {class_instance.the_class.studio} starting on {class_instance.start_time.strftime("%Y-%m-%d %H:%M")}'
            i += 1
        return Response(result)

class MyClassSchedule(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        enrolled_pairs = UserEnrolledClass.objects.filter(
            user_id=request.user.id)

        lst = []
        for pair in enrolled_pairs:
            class_id = pair.class_id
            class_instance = ClassInstance.objects.get(id=class_id)
            if class_instance.is_cancelled == False:
                lst.append(class_instance)

        n = len(lst)
        for i in range(1, n):
            key = lst[i]
            j = i - 1
            while (j >= 0 and lst[j].start_time > key.start_time):
                lst[j + 1] = lst[j]
                j = j - 1
            lst[j + 1] = key
        result = {}
        i = 1
        for class_instance in lst:
            result[i] = f'{class_instance.the_class.name} with id{class_instance.id} in {class_instance.the_class.studio} starting on {class_instance.start_time.strftime("%Y-%m-%d %H:%M")}'
            i += 1
        return Response(result)


class SearchByClassNameView(APIView):
    def get(self, request, *args, **kwargs):
        the_class = ClassInstance.objects.filter(the_class__studio=kwargs['studio'], the_class__name=kwargs['class'], is_cancelled=False)
        # cancelled classes will not be shown
        if the_class:
            i = 1
            result = {}
            for c in the_class:
                result[i] = c.get_class_info()
                i += 1
            return Response(result)
        raise Http404


class SearchByCoachView(APIView):
    def get(self, request, *args, **kwargs):
        the_class = Class.objects.filter(studio=kwargs['studio'], coach=kwargs['coach'])
        if the_class:
            i = 1
            result = {}
            for c in the_class:
                result[i] = c.name
                i += 1
            return Response(result)
        else:
            raise Http404


class SearchByDateView(APIView):
    def get(self, request, *args, **kwargs):
        year = kwargs['year']
        month = kwargs['month']
        day = kwargs['day']

        class_instances = ClassInstance.objects.filter(start_time__year=year,
                                                       start_time__month=month,
                                                       start_time__day=day,
                                                       the_class__studio=kwargs['studio'])
        if class_instances:
            i = 1
            result = {}
            for c in class_instances:
                result[i] = f'{c.the_class.name} with id{c.id}'
                i += 1
            return Response(result)
        else:
            raise Http404


class SearchByTimeRangeView(APIView):
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




