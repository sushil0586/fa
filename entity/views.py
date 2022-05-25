from django.http import request
from django.shortcuts import render

from rest_framework.generics import CreateAPIView,ListAPIView,ListCreateAPIView,RetrieveUpdateDestroyAPIView,GenericAPIView
from entity.models import entity,entity_details,unitType,entity_user
from entity.serializers import entitySerializer,entityDetailsSerializer,unitTypeSerializer,entityUserSerializer
from rest_framework import permissions
from django_filters.rest_framework import DjangoFilterBackend


class entityApiView(ListCreateAPIView):

    serializer_class = entitySerializer
    permission_classes = (permissions.IsAuthenticated,)

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id','unitType','entityName']

    def perform_create(self, serializer):
        return serializer.save(createdby = self.request.user)
    
    def get_queryset(self):
        return entity.objects.filter(createdby = self.request.user)

# class entityLoadApiView(ListCreateAPIView):

#     serializer_class = entitySerializer
#     permission_classes = (permissions.IsAuthenticated,)

#     filter_backends = [DjangoFilterBackend]
#     filterset_fields = ['id','unitType','entityName']

        
#     def get_queryset(self):
#         return entity.objects.filter()

class entityDetailsApiView(ListCreateAPIView):

    serializer_class = entityDetailsSerializer
    permission_classes = (permissions.IsAuthenticated,)

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['style']

    def perform_create(self, serializer):
        return serializer.save(owner = self.request.user)
    
    def get_queryset(self):
        return entity_details.objects.filter(owner = self.request.user)


class unitTypeApiView(ListCreateAPIView):

    serializer_class = unitTypeSerializer
    permission_classes = (permissions.IsAuthenticated,)

    filter_backends = [DjangoFilterBackend]
    #filterset_fields = ['id','unitType','entityName']

    def perform_create(self, serializer):
        return serializer.save(createdby = self.request.user)
    
    def get_queryset(self):
        return unitType.objects.filter()

class entityUserApiView(ListCreateAPIView):

    serializer_class = entityUserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id','entity',]


    

    def perform_create(self, serializer):
        return serializer.save(createdby = self.request.user)
    
    def get_queryset(self):

       # entity = entity_user.objects.filter(user = self.request.user).order_by('entity')[0]

    #print(entity)

       # entity = self.request.query_params.get('entity')
        return entity_user.objects.filter(user = self.request.user)