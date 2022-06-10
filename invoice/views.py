from django.http import request
from django.shortcuts import render

from rest_framework.generics import CreateAPIView,ListAPIView,ListCreateAPIView,RetrieveUpdateDestroyAPIView,GenericAPIView
from invoice.models import salesOrderdetails,SalesOderHeader,purchaseorder,PurchaseOrderDetails
from invoice.serializers import SalesOderHeaderSerializer,salesOrderdetailsSerializer,purchaseorderSerializer,PurchaseOrderDetailsSerializer,POSerializer
from rest_framework import permissions
from django_filters.rest_framework import DjangoFilterBackend
from django.db import DatabaseError, transaction
from rest_framework.response import Response


class SalesOderHeaderApiView(ListCreateAPIView):

    serializer_class = SalesOderHeaderSerializer
    permission_classes = (permissions.IsAuthenticated,)

    filter_backends = [DjangoFilterBackend]
    #filterset_fields = ['id','unitType','entityName']

    def perform_create(self, serializer):
        return serializer.save(owner = self.request.user)
    
    def get_queryset(self):
        entity = self.request.query_params.get('entity')
        return SalesOderHeader.objects.filter(entity = entity)


class salesOrderdetailsApiView(ListCreateAPIView):

    serializer_class = salesOrderdetailsSerializer
    permission_classes = (permissions.IsAuthenticated,)

    filter_backends = [DjangoFilterBackend]
    #filterset_fields = ['id','unitType','entityName']

    @transaction.atomic
    def perform_create(self, serializer):
        return serializer.save(owner = self.request.user)
    
    def get_queryset(self):
        return salesOrderdetails.objects.filter()

class salesOrderupdatedelview(RetrieveUpdateDestroyAPIView):

    serializer_class = SalesOderHeaderSerializer
    permission_classes = (permissions.IsAuthenticated,)
    lookup_field = "id"

    def get_queryset(self):
        entity = self.request.query_params.get('entity')
        return SalesOderHeader.objects.filter(entity = entity)



        ############################################################


class purchaseorderApiView(ListCreateAPIView):

    serializer_class = purchaseorderSerializer
    permission_classes = (permissions.IsAuthenticated,)

    filter_backends = [DjangoFilterBackend]
    #filterset_fields = ['id','unitType','entityName']

    def perform_create(self, serializer):
        return serializer.save(createdby = self.request.user)
    
    def get_queryset(self):
        entity = self.request.query_params.get('entity')
        return purchaseorder.objects.filter()


class PurchaseOrderDetailsApiView(ListCreateAPIView):

    serializer_class = PurchaseOrderDetailsSerializer
    permission_classes = (permissions.IsAuthenticated,)

    filter_backends = [DjangoFilterBackend]
    #filterset_fields = ['id','unitType','entityName']

    def perform_create(self, serializer):
        return serializer.save(createdby = self.request.user)
    
    def get_queryset(self):
        return PurchaseOrderDetails.objects.filter()


class purchaseorderupdatedelview(RetrieveUpdateDestroyAPIView):

    serializer_class = purchaseorderSerializer
    permission_classes = (permissions.IsAuthenticated,)
    lookup_field = "id"

    def get_queryset(self):
        entity = self.request.query_params.get('entity')
        return purchaseorder.objects.filter()

class purchaseordelatestview(ListCreateAPIView):

    serializer_class = POSerializer
    permission_classes = (permissions.IsAuthenticated,)

    filter_backends = [DjangoFilterBackend]
    #filterset_fields = ['id','unitType','entityName']

    # def perform_create(self, serializer):
    #     return serializer.save(createdby = self.request.user)

    def get(self,request):
        entity = self.request.query_params.get('entity')
        id = purchaseorder.objects.filter(entity= entity).last()
        serializer = POSerializer(id)
        return Response(serializer.data)
    
    # def get_queryset(self):
    #     entity = self.request.query_params.get('entity')
    #     po = purchaseorder.objects.get(pk=11)
    #     serializer = POSerializer(po)
    #     return Response(serializer.data)


# class purchaseordelatestview(RetrieveUpdateDestroyAPIView):

#     serializer_class = purchaseorderSerializer
#     permission_classes = (permissions.IsAuthenticated,)
#     # lookup_field = "id"

#     def get_queryset(self):
#         entity = self.request.query_params.get('entity')
#         return purchaseorder.objects.latest('VoucherNo')