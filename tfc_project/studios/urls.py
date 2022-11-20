# -*- coding: utf-8 -*-
# Copyright (c) CDU

"""Model Docstrings

"""

from django.urls import path

from .views import StudioView, DistanceView

urlpatterns = [
    path('distance', DistanceView.as_view()),
    path('query', StudioView.as_view())


]
