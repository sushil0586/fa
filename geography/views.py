from django.http import request
from django.shortcuts import render

from rest_framework.generics import CreateAPIView,ListAPIView,ListCreateAPIView,RetrieveUpdateDestroyAPIView,GenericAPIView
from geography.models import country,state,district,city
from geography.serializers import countrySerializer,stateListSerializer,districtListSerializer,cityListSerializer
from rest_framework import permissions
from django_filters.rest_framework import DjangoFilterBackend


class countryApiView(ListAPIView):

    serializer_class = countrySerializer
    permission_classes = (permissions.IsAuthenticated,)

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id']

    
    
    def get_queryset(self):
        return country.objects.all()

class stateApiView(ListAPIView):

    serializer_class = stateListSerializer
    permission_classes = (permissions.IsAuthenticated,)

    
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id','country',]
    
    def get_queryset(self):
        return state.objects.all()

class districtApiView(ListAPIView):

    serializer_class = districtListSerializer
    permission_classes = (permissions.IsAuthenticated,)

    
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id','state',]
    
    def get_queryset(self):
        return district.objects.all()

class cityApiView(ListAPIView):

    serializer_class = cityListSerializer
    permission_classes = (permissions.IsAuthenticated,)

    
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id','distt']
    
    def get_queryset(self):
        return city.objects.filter()

