# -*- coding: utf-8 -*-
# Copyright (c) CDU

"""Model Docstrings

"""

from django.urls import path

from .views import StudioView, DistanceView,DistanceClass,ShowClassInStudioView

urlpatterns = [
    path('distance', DistanceView.as_view()),
    path('query', StudioView.as_view()),
    path('cal_distance', DistanceClass.as_view()),
    path('get_classes', ShowClassInStudioView.as_view()),


]
