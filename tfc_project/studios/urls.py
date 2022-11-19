# -*- coding: utf-8 -*-
# Copyright (c) CDU

"""Model Docstrings

"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from django.urls import path

from .views import StudioView, DistanceView

urlpatterns = [
    path('distance', DistanceView.as_view()),
    path('query', StudioView.as_view())


]
