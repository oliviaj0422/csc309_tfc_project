from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Card, Payment

admin.site.register(CustomUser, UserAdmin)
admin.site.register(Card)
admin.site.register(Payment)


