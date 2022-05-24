from django.http import request
from django.shortcuts import render

from rest_framework.generics import CreateAPIView,ListAPIView,ListCreateAPIView,RetrieveUpdateDestroyAPIView
from inventory.models import Album, Product, Track
from inventory.serializers import ProductSerializer,AlbumSerializer,Trackserializer
from rest_framework import permissions
from django_filters.rest_framework import DjangoFilterBackend


class CreateTodoApiView(CreateAPIView):
    serializer_class = ProductSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        return serializer.save(owner = self.request.user)


class ListproductApiView(ListAPIView):

    serializer_class = ProductSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Product.objects.filter(owner = self.request.user)

class productApiView(ListCreateAPIView):

    serializer_class = ProductSerializer
    permission_classes = (permissions.IsAuthenticated,)

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id','ProductName','is_stockable']

    def perform_create(self, serializer):
        return serializer.save(owner = self.request.user)
    
    def get_queryset(self):
        return Product.objects.filter(owner = self.request.user)

class productupdatedel(RetrieveUpdateDestroyAPIView):

    serializer_class = ProductSerializer
    permission_classes = (permissions.IsAuthenticated,)
    lookup_field = "id"

    def get_queryset(self):
        return Product.objects.filter(owner = self.request.user)


class AlbumApiView(ListCreateAPIView):

    serializer_class = AlbumSerializer
    permission_classes = (permissions.IsAuthenticated,)

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id','album_name', 'artist', 'tracks']

    def perform_create(self, serializer):
        return serializer.save(owner = self.request.user)
    
    def get_queryset(self):
        return Album.objects.filter(owner = self.request.user)


class Albumupdatedel(RetrieveUpdateDestroyAPIView):

    serializer_class = AlbumSerializer
    permission_classes = (permissions.IsAuthenticated,)
    lookup_field = "id"

    def get_queryset(self):
        return Album.objects.filter(owner = self.request.user)


class TrackApiView(ListCreateAPIView):

    serializer_class = Trackserializer
    permission_classes = (permissions.IsAuthenticated,)

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id','album','order','title','duration']

    def perform_create(self, serializer):
        return serializer.save(owner = self.request.user)
    
    def get_queryset(self):
        return Track.objects.filter(owner = self.request.user)







