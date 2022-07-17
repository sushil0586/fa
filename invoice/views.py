from django.http import request
from django.shortcuts import render

from rest_framework.generics import CreateAPIView,ListAPIView,ListCreateAPIView,RetrieveUpdateDestroyAPIView,GenericAPIView,RetrieveAPIView
from invoice.models import salesOrderdetails,SalesOderHeader,purchaseorder,PurchaseOrderDetails,journal,salereturn,salereturnDetails,PurchaseReturn,Purchasereturndetails,StockTransactions,journalmain,entry,stockdetails,stockmain,goodstransaction
from invoice.serializers import SalesOderHeaderSerializer,salesOrderdetailsSerializer,purchaseorderSerializer,PurchaseOrderDetailsSerializer,POSerializer,SOSerializer,journalSerializer,SRSerializer,salesreturnSerializer,salesreturnDetailsSerializer,JournalVSerializer,PurchasereturnSerializer,\
purchasereturndetailsSerializer,PRSerializer,TrialbalanceSerializer,TrialbalanceSerializerbyaccounthead,TrialbalanceSerializerbyaccount,accountheadserializer,accountHead,accountserializer,accounthserializer, stocktranserilaizer,cashserializer,journalmainSerializer,stockdetailsSerializer,stockmainSerializer,\
PRSerializer,SRSerializer,stockVSerializer,stockserializer
from rest_framework import permissions
from django_filters.rest_framework import DjangoFilterBackend
from django.db import DatabaseError, transaction
from rest_framework.response import Response
from django.db.models import Sum,OuterRef,Subquery,F
from django.db.models import Prefetch
from financial.models import account
from inventory.models import Product


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


class salesOrderpreviousview(RetrieveAPIView):

    serializer_class = SalesOderHeaderSerializer
    permission_classes = (permissions.IsAuthenticated,)
    lookup_field = "billno"

    def get_queryset(self):
        entity = self.request.query_params.get('entity')
        #billno = self.request.query_params.get('billno')
        return SalesOderHeader.objects.filter(entity = entity)



class salesorderlatestview(ListCreateAPIView):

    serializer_class = SOSerializer
    permission_classes = (permissions.IsAuthenticated,)

    filter_backends = [DjangoFilterBackend]
    #filterset_fields = ['id','unitType','entityName']

    # def perform_create(self, serializer):
    #     return serializer.save(createdby = self.request.user)

    def get(self,request):
        entity = self.request.query_params.get('entity')
        id = SalesOderHeader.objects.filter(entity= entity).last()
        serializer = SOSerializer(id)
        return Response(serializer.data)




class purchasereturnlatestview(ListCreateAPIView):

    serializer_class = PRSerializer
    permission_classes = (permissions.IsAuthenticated,)

    filter_backends = [DjangoFilterBackend]
    #filterset_fields = ['id','unitType','entityName']

    # def perform_create(self, serializer):
    #     return serializer.save(createdby = self.request.user)

    def get(self,request):
        entity = self.request.query_params.get('entity')
        id = PurchaseReturn.objects.filter(entity= entity).last()
        serializer = PRSerializer(id)
        return Response(serializer.data)


class PurchaseReturnApiView(ListCreateAPIView):

    serializer_class = PurchasereturnSerializer
    permission_classes = (permissions.IsAuthenticated,)

    filter_backends = [DjangoFilterBackend]
    #filterset_fields = ['id','unitType','entityName']

    def perform_create(self, serializer):
        return serializer.save(owner = self.request.user)
    
    def get_queryset(self):
        entity = self.request.query_params.get('entity')
        return PurchaseReturn.objects.filter(entity = entity)


class PurchaseReturnupdatedelview(RetrieveUpdateDestroyAPIView):

    serializer_class = PurchasereturnSerializer
    permission_classes = (permissions.IsAuthenticated,)
    lookup_field = "id"

    def get_queryset(self):
        entity = self.request.query_params.get('entity')
        return PurchaseReturn.objects.filter(entity = entity)


class PurchaseReturnpreviousview(RetrieveAPIView):

    serializer_class = PurchasereturnSerializer
    permission_classes = (permissions.IsAuthenticated,)
    lookup_field = "billno"

    def get_queryset(self):
        entity = self.request.query_params.get('entity')
        #billno = self.request.query_params.get('billno')
        return PurchaseReturn.objects.filter(entity = entity)

class PurchaseReturnlatestview(ListCreateAPIView):

    serializer_class = PRSerializer
    permission_classes = (permissions.IsAuthenticated,)

    filter_backends = [DjangoFilterBackend]
    #filterset_fields = ['id','unitType','entityName']

    # def perform_create(self, serializer):
    #     return serializer.save(createdby = self.request.user)

    def get(self,request):
        entity = self.request.query_params.get('entity')
        id = PurchaseReturn.objects.filter(entity= entity).last()
        serializer = PRSerializer(id)
        return Response(serializer.data)






        ############################################################


class purchaseorderApiView(ListCreateAPIView):

    serializer_class = purchaseorderSerializer
    permission_classes = (permissions.IsAuthenticated,)

    filter_backends = [DjangoFilterBackend]
    #filterset_fields = ['id','unitType','entityName']
    @transaction.atomic
    def perform_create(self, serializer):
        return serializer.save(createdby = self.request.user)
    
    def get_queryset(self):
        entity = self.request.query_params.get('entity')
        return purchaseorder.objects.filter(entity = entity)


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


class purchaseorderpreviousview(RetrieveUpdateDestroyAPIView):

    serializer_class = purchaseorderSerializer
    permission_classes = (permissions.IsAuthenticated,)
    lookup_field = "voucherno"

    def get_queryset(self):
        entity = self.request.query_params.get('entity')
        return purchaseorder.objects.filter()

class purchaseordelatestview(ListCreateAPIView):

    serializer_class = POSerializer
    permission_classes = (permissions.IsAuthenticated,)

    filter_backends = [DjangoFilterBackend]
    def get(self,request):
        entity = self.request.query_params.get('entity')
        id = purchaseorder.objects.filter(entity= entity).last()
        serializer = POSerializer(id)
        return Response(serializer.data)



class purchaseordelatestview(ListCreateAPIView):

    serializer_class = POSerializer
    permission_classes = (permissions.IsAuthenticated,)

    filter_backends = [DjangoFilterBackend]
    def get(self,request):
        entity = self.request.query_params.get('entity')
        id = purchaseorder.objects.filter(entity= entity).last()
        serializer = POSerializer(id)
        return Response(serializer.data)



        

class journalordelatestview(ListCreateAPIView):

    serializer_class = JournalVSerializer
    permission_classes = (permissions.IsAuthenticated,)

    filter_backends = [DjangoFilterBackend]
    def get(self,request):
        entity = self.request.query_params.get('entity')
        id = journalmain.objects.filter(entity= entity,vouchertype = 'J').last()
        serializer = JournalVSerializer(id)
        return Response(serializer.data)


class stockordelatestview(ListCreateAPIView):

    serializer_class = stockVSerializer
    permission_classes = (permissions.IsAuthenticated,)

    filter_backends = [DjangoFilterBackend]
    def get(self,request):
        entity = self.request.query_params.get('entity')
        id = stockmain.objects.filter(entity= entity,vouchertype = 'PC').last()
        serializer = stockVSerializer(id)
        return Response(serializer.data)


class bankordelatestview(ListCreateAPIView):

    serializer_class = JournalVSerializer
    permission_classes = (permissions.IsAuthenticated,)

    filter_backends = [DjangoFilterBackend]
    def get(self,request):
        entity = self.request.query_params.get('entity')
        id = journalmain.objects.filter(entity= entity,vouchertype = 'B').last()
        serializer = JournalVSerializer(id)
        return Response(serializer.data)


class cashordelatestview(ListCreateAPIView):

    serializer_class = JournalVSerializer
    permission_classes = (permissions.IsAuthenticated,)

    filter_backends = [DjangoFilterBackend]
    def get(self,request):
        entity = self.request.query_params.get('entity')
        id = journalmain.objects.filter(entity= entity,vouchertype = 'C').last()
        serializer = JournalVSerializer(id)
        return Response(serializer.data)



class salesreturnApiView(ListCreateAPIView):

    serializer_class = salesreturnSerializer
    permission_classes = (permissions.IsAuthenticated,)

    filter_backends = [DjangoFilterBackend]
    #filterset_fields = ['id','unitType','entityName']

    @transaction.atomic
    def perform_create(self, serializer):
        return serializer.save(createdby = self.request.user)
    
    def get_queryset(self):
        entity = self.request.query_params.get('entity')
        return salereturn.objects.filter(entity = entity)



class journalmainApiView(ListCreateAPIView):

    serializer_class = journalmainSerializer
    permission_classes = (permissions.IsAuthenticated,)

    filter_backends = [DjangoFilterBackend]
    #filterset_fields = ['id','unitType','entityName']

    @transaction.atomic
    def perform_create(self, serializer):
        return serializer.save(createdby = self.request.user)
    
    def get_queryset(self):
        entity = self.request.query_params.get('entity')
        return journalmain.objects.filter(entity = entity)



class journalmainupdateapiview(RetrieveUpdateDestroyAPIView):

    serializer_class = journalmainSerializer
    permission_classes = (permissions.IsAuthenticated,)
    lookup_field = "id"

    def get_queryset(self):
        entity = self.request.query_params.get('entity')
        return journalmain.objects.filter(entity = entity)




class stockmainApiView(ListCreateAPIView):

    serializer_class = stockmainSerializer
    permission_classes = (permissions.IsAuthenticated,)

    filter_backends = [DjangoFilterBackend]
    #filterset_fields = ['id','unitType','entityName']

    @transaction.atomic
    def perform_create(self, serializer):
        return serializer.save(createdby = self.request.user)
    
    def get_queryset(self):
        entity = self.request.query_params.get('entity')
        return stockmain.objects.filter(entity = entity)



class stockmainupdateapiview(RetrieveUpdateDestroyAPIView):

    serializer_class = stockmainSerializer
    permission_classes = (permissions.IsAuthenticated,)
    lookup_field = "id"

    def get_queryset(self):
        entity = self.request.query_params.get('entity')
        return stockmain.objects.filter(entity = entity)



class journalmainpreviousapiview(RetrieveUpdateDestroyAPIView):

    serializer_class = journalmainSerializer
    permission_classes = (permissions.IsAuthenticated,)
    lookup_field = "voucherno"

    def get_queryset(self):
        entity = self.request.query_params.get('entity')
        vouchertype = self.request.query_params.get('vouchertype')
        return journalmain.objects.filter(entity = entity,vouchertype=vouchertype)


class stockmainpreviousapiview(RetrieveUpdateDestroyAPIView):

    serializer_class = stockmainSerializer
    permission_classes = (permissions.IsAuthenticated,)
    lookup_field = "voucherno"

    def get_queryset(self):
        entity = self.request.query_params.get('entity')
       # vouchertype = self.request.query_params.get('vouchertype')
        return stockmain.objects.filter(entity = entity)





class salesreturnlatestview(ListCreateAPIView):

    serializer_class = SRSerializer
    permission_classes = (permissions.IsAuthenticated,)

    filter_backends = [DjangoFilterBackend]
    def get(self,request):
        entity = self.request.query_params.get('entity')
        id = salereturn.objects.filter(entity= entity).last()
        serializer = SRSerializer(id)
        return Response(serializer.data)


class salesreturnupdatedelview(RetrieveUpdateDestroyAPIView):

    serializer_class = salesreturnSerializer
    permission_classes = (permissions.IsAuthenticated,)
    lookup_field = "id"

    def get_queryset(self):
        entity = self.request.query_params.get('entity')
        return salereturn.objects.filter()


class salesreturnpreviousview(RetrieveUpdateDestroyAPIView):

    serializer_class = salesreturnSerializer
    permission_classes = (permissions.IsAuthenticated,)
    lookup_field = "voucherno"

    def get_queryset(self):
        entity = self.request.query_params.get('entity')
        return salereturn.objects.filter()
    




class JournalApiView(ListCreateAPIView):

    serializer_class = journalSerializer
    permission_classes = (permissions.IsAuthenticated,)

    filter_backends = [DjangoFilterBackend]
    #filterset_fields = ['id','unitType','entityName']


    def create(self, request, *args, **kwargs):  

        serializer = self.get_serializer(data=request.data, many=True)  
        serializer.is_valid(raise_exception=True)  
  
        try:  
            serializer.save(createdby = self.request.user)
           # self.perform_create(serializer)  
            return Response(serializer.data)  
        except:  
            return Response(serializer.errors)  

    # def perform_create(self, serializer):
    #     return serializer.save(createdby = self.request.user)
    
    def get_queryset(self):
        entity = self.request.query_params.get('entity')
        return journal.objects.filter(entity = entity)


class TrialbalanceApiView(ListAPIView):

    serializer_class = TrialbalanceSerializer
    permission_classes = (permissions.IsAuthenticated,)

    filter_backends = [DjangoFilterBackend]
    #filterset_fields = ['id','unitType','entityName']
    def get_queryset(self):
        #entity = self.request.query_params.get('entity')
        entity = self.request.query_params.get('entity')
        stk =StockTransactions.objects.filter(entity = entity).values('account__accounthead__name','account__accounthead').annotate(debit = Sum('debitamount'),credit = Sum('creditamount') )
        return stk


class TrialbalancebyaccountheadApiView(ListAPIView):

    serializer_class = TrialbalanceSerializerbyaccounthead
    permission_classes = (permissions.IsAuthenticated,)

    filter_backends = [DjangoFilterBackend]
    #filterset_fields = ['id','unitType','entityName']


    
    def get_queryset(self):
        #entity = self.request.query_params.get('entity')
        entity = self.request.query_params.get('entity')
        accounthead = self.request.query_params.get('accounthead')
        stk =StockTransactions.objects.filter(entity = entity,accounthead = accounthead).values('account__accountname','account').annotate(debit = Sum('debitamount'),credit = Sum('creditamount') )
        #print(stk)
        return stk

class TrialbalancebyaccountApiView(ListAPIView):

    serializer_class = TrialbalanceSerializerbyaccount
    permission_classes = (permissions.IsAuthenticated,)

    filter_backends = [DjangoFilterBackend]
    #filterset_fields = ['id','unitType','entityName']


    
    def get_queryset(self):
        #entity = self.request.query_params.get('entity')
        entity = self.request.query_params.get('entity')
        account = self.request.query_params.get('account')
        stk =StockTransactions.objects.filter(entity = entity,account = account).values('account__accountname','transactiontype','transactionid','entrydatetime','desc').annotate(debit = Sum('debitamount'),credit = Sum('creditamount') )
        #print(stk)
        return stk



class Trialview(ListAPIView):

    serializer_class = accountheadserializer
  #  filter_class = accountheadFilter
    permission_classes = (permissions.IsAuthenticated,)

    filter_backends = [DjangoFilterBackend]
    #filterset_fields = ['id','unitType','entityName']
    def get_queryset(self):
        #entity = self.request.query_params.get('entity')
        entity = self.request.query_params.get('entity')

        # stk = accountHead.objects.prefetch_related(Prefetch('headtrans',queryset = account.objects.prefetch_related(Prefetch('headtrans', queryset=StockTransactions.objects.filter(
        #         entity=entity).order_by('entity'))))to_attr='accounthead_transactions')

        
        stk = accountHead.objects.prefetch_related(Prefetch('headtrans', queryset=StockTransactions.objects.filter(
                entity=entity).order_by('entity'), to_attr='accounthead_transactions')
        )
        
        return stk



class Trialviewaccount(ListAPIView):

    serializer_class = accountserializer
  #  filter_class = accountheadFilter
    permission_classes = (permissions.IsAuthenticated,)

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id']
    def get_queryset(self):
        #account = self.request.query_params.get('account')
        entity = self.request.query_params.get('entity')

        queryset1=StockTransactions.objects.filter(entity=entity).order_by('entity').only('account__accountname','transactiontype','transactionid','entrydatetime','desc','debitamount','creditamount')

        queryset=account.objects.prefetch_related(Prefetch('accounttrans', queryset=queryset1,to_attr='account_transactions'))

        
        #stk = account.objects.prefetch_related(Prefetch('accounthead_accounts', queryset=queryset1, to_attr='account_transactions')
        
     
        return queryset

    


class daybookviewapi(ListAPIView):

    serializer_class = cashserializer
  #  filter_class = accountheadFilter
    permission_classes = (permissions.IsAuthenticated,)

    filter_backends = [DjangoFilterBackend]
    #filterset_fields = ['id']
    def get_queryset(self):
        #account = self.request.query_params.get('account')
        entity = self.request.query_params.get('entity')



        queryset1=StockTransactions.objects.filter(entity=entity).order_by('entity').only('account__accountname','transactiontype','transactionid','entrydatetime','desc','debitamount','creditamount')

        queryset=entry.objects.prefetch_related(Prefetch('cashtrans', queryset=queryset1,to_attr='account_transactions'))

        print(queryset)
        print('account_transactions')

     
        
     
        return queryset




class stockviewapi(ListAPIView):

    serializer_class = stockserializer
  #  filter_class = accountheadFilter
    permission_classes = (permissions.IsAuthenticated,)

    filter_backends = [DjangoFilterBackend]
    #filterset_fields = ['id']
    def get_queryset(self):
        #account = self.request.query_params.get('account')
        entity = self.request.query_params.get('entity')



        queryset1=goodstransaction.objects.filter(entity=entity).order_by('entity').only('account__accountname','stock__productname','transactiontype','transactionid','entrydatetime')

        queryset=Product.objects.filter(entity=entity).prefetch_related(Prefetch('goods', queryset=queryset1,to_attr='account_transactions'))

        print(queryset)
        print('account_transactions')

     
        
     
        return queryset

