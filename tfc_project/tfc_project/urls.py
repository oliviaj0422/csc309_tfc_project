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
from django.shortcuts import redirect
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView

from accounts.views import CreateUserView, CreateCardView, \
    CustomTokenObtainPairView, EditProfileView, \
    UpdateCardView, PaymentHistoryView, MembershipView, SingleProfileView, \
    DeleteCardView



urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('account/signup/', CreateUserView.as_view()),
    path('account/add_payment_method/', CreateCardView.as_view()),
    path('account/<int:pk>/profile/', SingleProfileView.as_view()),
    path('account/<int:pk>/profile/edit/', EditProfileView.as_view()),
    path('account/<int:pk>/profile/update_card_info/', UpdateCardView.as_view()),
    path('account/<int:pk>/profile/delete_card/', DeleteCardView.as_view()),
    path('account/payment_history/', PaymentHistoryView.as_view()),
    path('memberships/', MembershipView.as_view()),
    path('classes/', include('classes.urls')),
    path('studios/', include('studios.urls')),
    path('', lambda r: redirect('/admin'))
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


