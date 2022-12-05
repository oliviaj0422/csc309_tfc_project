from django.contrib import admin

# Register your models here.
from classes.models import Class,ClassInstance,UserEnrolledClass
admin.site.register(Class)
admin.site.register(ClassInstance)
admin.site.register(UserEnrolledClass)
