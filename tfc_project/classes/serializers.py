from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from classes.models import ClassInstance,UserEnrolledClass

class ClassInstanceSerializer(ModelSerializer):
    class Meta:
        model = ClassInstance
        fields = ['id','class_name', 'description','coach','keywords','space_availability', 'start_time', 'end_time','is_cancelled']

class UserEnrolledClassSerializer(ModelSerializer):
    class Meta:
        model = UserEnrolledClass
        fields=['class_instance_name','class_instance','class_instance_start_time','class_instance_end_time']
