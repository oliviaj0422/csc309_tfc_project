from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView, ListAPIView, \
    CreateAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated


