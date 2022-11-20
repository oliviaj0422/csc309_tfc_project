"""tfc_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.urls import path
from django.urls import re_path
from django.views.i18n import JavaScriptCatalog
from accounts.views import CreateUserView, CreateCardView, EditProfileView, \
    UpdateCardView
from rest_framework_simplejwt.views import TokenObtainPairView
from django.shortcuts import redirect
urlpatterns = [
    path('admin/', admin.site.urls),
    path('classes/', include('classes.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('account/signup/', CreateUserView.as_view()),
    path('account/add_payment_method/', CreateCardView.as_view()),
    path('account/<int:pk>/profile/edit/', EditProfileView.as_view()),
    path('account/<int:pk>/profile/card_info/update/', UpdateCardView.as_view()),
    path('studios/', include('studios.urls')),
    path('', lambda r: redirect('/admin'))
]

js_info_dict = {
    'packages': ('recurrence', ),
}

# jsi18n can be anything you like here
urlpatterns += [
    re_path(r'^jsi18n/$', JavaScriptCatalog.as_view(), js_info_dict),
]
