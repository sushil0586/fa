
import imp
from itertools import product
from rest_framework import serializers
from invoice.models import SalesOderHeader,salesOrderdetails,purchaseorder,PurchaseOrderDetails,\
    journal,salereturn,salereturnDetails,Transactions,StockTransactions,PurchaseReturn,Purchasereturndetails
from financial.models import account,accountHead
from inventory.models import Product
from django.db.models import Sum,Count



class salesOrderdetailsSerializer(serializers.ModelSerializer):
    #entityUser = entityUserSerializer(many=True)
    id = serializers.IntegerField(required=False)

    class Meta:
        model = salesOrderdetails
        fields =  ('id','product','orderqty','pieces','rate','amount','cgst','sgst','igst','linetotal','entity',)


class SalesOderHeaderSerializer(serializers.ModelSerializer):
    salesorderdetails = salesOrderdetailsSerializer(many=True)

    class Meta:
        model = SalesOderHeader
        fields = ('id','sorderdate','billno','accountid','latepaymentalert','grno','vehicle','taxtype','billcash','supply','shippedto','remarks','transport','broker','tds194q','tcs206c1ch1','tcs206c1ch2','tcs206c1ch3','tcs206C1','tcs206C2','duedate','subtotal','subtotal','cgst','sgst','igst','expenses','gtotal','entity','owner','salesorderdetails',)


    def createtransaction(self,order):
        id = order.id
        subtotal = order.subtotal
        cgst = order.cgst
        sgst = order.sgst
        igst = order.igst
        gtotal = order.gtotal
        pentity = order.entity
        purchaseid = account.objects.get(entity =pentity,accountcode = 3000)
        cgstid = account.objects.get(entity =pentity,accountcode = 6001)
        sgstid = account.objects.get(entity =pentity,accountcode = 6002)
        igstid = account.objects.get(entity =pentity,accountcode = 6003)
        StockTransactions.objects.create(accounthead = cgstid.accounthead, account= cgstid,transactiontype = 'S',transactionid = id,desc = 'Sale By B.No ' + str(order.billno),drcr=0,creditamount=cgst,entity=pentity,createdby= order.owner)
        StockTransactions.objects.create(accounthead = sgstid.accounthead,account= sgstid,transactiontype = 'S',transactionid = id,desc = 'Sale By B.No ' + str(order.billno),drcr=0,creditamount=sgst,entity=pentity,createdby= order.owner)
        StockTransactions.objects.create(accounthead= order.accountid.accounthead,account= order.accountid,transactiontype = 'S',transactionid = id,desc = 'Sale By B.No ' + str(order.billno),drcr=1,debitamount=gtotal,entity=pentity,createdby= order.owner)
        return id

    def create(self, validated_data):
        #print(validated_data)
        salesOrderdetails_data = validated_data.pop('salesorderdetails')
        order = SalesOderHeader.objects.create(**validated_data)
        #print(tracks_data)
        for PurchaseOrderDetail_data in salesOrderdetails_data:
            detail = salesOrderdetails.objects.create(salesorderheader = order, **PurchaseOrderDetail_data)
            if(detail.orderqty ==0.00):
                qty = detail.pieces
            else:
                qty = detail.orderqty
            StockTransactions.objects.create(accounthead = detail.product.saleaccount.accounthead,account= detail.product.saleaccount,stock=detail.product,transactiontype = 'S',transactionid = detail.id,desc = 'Sale By B.No ' + str(order.billno),stockttype = 'S',salequantity = qty,drcr = 0,creditamount = detail.amount,cgstcr = detail.cgst,sgstcr= detail.sgst,igstcr = detail.igst,entrydate = order.sorderdate,entity = order.entity,createdby = order.owner)

        self.createtransaction(order)
        return order

    def update(self, instance, validated_data):
        fields = ['sorderdate','billno','accountid','latepaymentalert','grno','vehicle','taxtype','billcash','supply','shippedto','remarks','transport','broker','tds194q','tcs206c1ch1','tcs206c1ch2','tcs206c1ch3','tcs206C1','tcs206C2','duedate','subtotal','subtotal','cgst','sgst','igst','expenses','gtotal','entity','owner',]
        for field in fields:
            try:
                setattr(instance, field, validated_data[field])
            except KeyError:  # validated_data may not contain all fields during HTTP PATCH
                pass
        instance.save()

        items = validated_data.get('salesorderdetails')

        product_items_dict = dict((i.id, i) for i in instance.salesorderdetails.all())
        print(product_items_dict)

        for item in items:
            item_id = item.get('id', None)
            if item_id:



                product_items_dict.pop(item_id)
                inv_item = salesOrderdetails.objects.get(id=item_id, salesorderheader=instance)
                inv_item.product = item.get('product', inv_item.product)
                inv_item.orderqty = item.get('orderqty', inv_item.orderqty)
                inv_item.pieces = item.get('pieces', inv_item.pieces)
                inv_item.rate = item.get('rate', inv_item.rate)
                inv_item.amount = item.get('amount', inv_item.amount)
                inv_item.cgst = item.get('cgst', inv_item.cgst)
                inv_item.sgst = item.get('sgst', inv_item.sgst)
                inv_item.igst = item.get('igst', inv_item.igst)
                inv_item.linetotal = item.get('linetotal', inv_item.linetotal)
                inv_item.entity = item.get('entity', inv_item.entity)
                inv_item.save()
            else:
                salesOrderdetails.objects.create(salesorderheader=instance, **item)


        if len(product_items_dict) > 0:
            for item in product_items_dict.values():
                item.delete()
        return instance

class SOSerializer(serializers.ModelSerializer):
    #entityUser = entityUserSerializer(many=True)
  #  id = serializers.IntegerField(required=False)

    newbillno = serializers.SerializerMethodField()

    def get_newbillno(self, obj):
        if not obj.billno :
            return 1
        else:
            return obj.billno + 1


    class Meta:
        model = SalesOderHeader
        fields =  ['newbillno']


class purchasereturndetailsSerializer(serializers.ModelSerializer):
    #entityUser = entityUserSerializer(many=True)
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Purchasereturndetails
        fields =  ('id','product','orderqty','pieces','rate','amount','cgst','sgst','igst','linetotal','entity',)


class PurchasereturnSerializer(serializers.ModelSerializer):
    purchasereturndetails = purchasereturndetailsSerializer(many=True)

    class Meta:
        model = PurchaseReturn
        fields = ('id','sorderdate','billno','accountid','latepaymentalert','grno','vehicle','taxtype','billcash','supply','shippedto','remarks','transport','broker','tds194q','tcs206c1ch1','tcs206c1ch2','tcs206c1ch3','tcs206C1','tcs206C2','duedate','subtotal','subtotal','cgst','sgst','igst','expenses','gtotal','entity','owner','purchasereturndetails',)


    def createtransaction(self,order):
        id = order.id
        subtotal = order.subtotal
        cgst = order.cgst
        sgst = order.sgst
        igst = order.igst
        gtotal = order.gtotal
        pentity = order.entity
        purchaseid = account.objects.get(entity =pentity,accountcode = 3000)
        cgstid = account.objects.get(entity =pentity,accountcode = 6001)
        sgstid = account.objects.get(entity =pentity,accountcode = 6002)
        igstid = account.objects.get(entity =pentity,accountcode = 6003)
        StockTransactions.objects.create(accounthead = cgstid.accounthead, account= cgstid,transactiontype = 'PR',transactionid = id,desc = 'Purchase return By V.No ' + str(order.billno),drcr=0,creditamount=cgst,entity=pentity,createdby= order.owner)
        StockTransactions.objects.create(accounthead = sgstid.accounthead,account= sgstid,transactiontype = 'PR',transactionid = id,desc = 'Purchase return By V.No ' + str(order.billno),drcr=0,creditamount=sgst,entity=pentity,createdby= order.owner)
        StockTransactions.objects.create(accounthead= order.accountid.accounthead,account= order.accountid,transactiontype = 'PR',transactionid = id,desc = 'Purchase return By V.No ' + str(order.billno),drcr=1,debitamount=gtotal,entity=pentity,createdby= order.owner)
        return id

    def create(self, validated_data):
        #print(validated_data)
        salesOrderdetails_data = validated_data.pop('purchasereturndetails')
        order = PurchaseReturn.objects.create(**validated_data)
        #print(tracks_data)
        for PurchaseOrderDetail_data in salesOrderdetails_data:
            detail = Purchasereturndetails.objects.create(purchasereturn = order, **PurchaseOrderDetail_data)
            if(detail.orderqty ==0.00):
                qty = detail.pieces
            else:
                qty = detail.orderqty
            StockTransactions.objects.create(accounthead = detail.product.saleaccount.accounthead,account= detail.product.saleaccount,stock=detail.product,transactiontype = 'PR',transactionid = detail.id,desc = 'Purchase return By V.No ' + str(order.billno),stockttype = 'S',salequantity = qty,drcr = 0,creditamount = detail.amount,cgstcr = detail.cgst,sgstcr= detail.sgst,igstcr = detail.igst,entrydate = order.sorderdate,entity = order.entity,createdby = order.owner)

        self.createtransaction(order)
        return order

    def update(self, instance, validated_data):
        fields = ['sorderdate','billno','accountid','latepaymentalert','grno','vehicle','taxtype','billcash','supply','shippedto','remarks','transport','broker','tds194q','tcs206c1ch1','tcs206c1ch2','tcs206c1ch3','tcs206C1','tcs206C2','duedate','subtotal','subtotal','cgst','sgst','igst','expenses','gtotal','entity','owner',]
        for field in fields:
            try:
                setattr(instance, field, validated_data[field])
            except KeyError:  # validated_data may not contain all fields during HTTP PATCH
                pass
        instance.save()

        items = validated_data.get('purchasereturndetails')

        product_items_dict = dict((i.id, i) for i in instance.purchasereturndetails.all())
        print(product_items_dict)

        for item in items:
            item_id = item.get('id', None)
            if item_id:



                product_items_dict.pop(item_id)
                inv_item = Purchasereturndetails.objects.get(id=item_id, purchasereturn=instance)
                inv_item.product = item.get('product', inv_item.product)
                inv_item.orderqty = item.get('orderqty', inv_item.orderqty)
                inv_item.pieces = item.get('pieces', inv_item.pieces)
                inv_item.rate = item.get('rate', inv_item.rate)
                inv_item.amount = item.get('amount', inv_item.amount)
                inv_item.cgst = item.get('cgst', inv_item.cgst)
                inv_item.sgst = item.get('sgst', inv_item.sgst)
                inv_item.igst = item.get('igst', inv_item.igst)
                inv_item.linetotal = item.get('linetotal', inv_item.linetotal)
                inv_item.entity = item.get('entity', inv_item.entity)
                inv_item.save()
            else:
                Purchasereturndetails.objects.create(purchasereturn=instance, **item)


        if len(product_items_dict) > 0:
            for item in product_items_dict.values():
                item.delete()
        return instance

class PRSerializer(serializers.ModelSerializer):
    #entityUser = entityUserSerializer(many=True)
  #  id = serializers.IntegerField(required=False)

    newbillno = serializers.SerializerMethodField()

    def get_newbillno(self, obj):
        if not obj.billno :
            return 1
        else:
            return obj.billno + 1


    class Meta:
        model = PurchaseReturn
        fields =  ['newbillno']




class POSerializer(serializers.ModelSerializer):
    #entityUser = entityUserSerializer(many=True)
  #  id = serializers.IntegerField(required=False)

    newvoucher = serializers.SerializerMethodField()

    def get_newvoucher(self, obj):
        if not obj.voucherno:
            return 1
        else:
            return obj.voucherno + 1


    class Meta:
        model = purchaseorder
        fields =  ['newvoucher']




class PurchaseOrderDetailsSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    #entityUser = entityUserSerializer(many=True)

    class Meta:
        model = PurchaseOrderDetails
        fields = ('id','product', 'purchasedesc','orderqty','pieces','rate','amount','cgst','sgst','igst','linetotal','entity',)






class purchaseorderSerializer(serializers.ModelSerializer):
    purchaseorderdetails = PurchaseOrderDetailsSerializer(many=True)

    class Meta:
        model = purchaseorder
        fields = ('id','voucherdate','voucherno','account','billno','billdate','terms','taxtype','billcash','subtotal','cgst','sgst','igst','expenses','gtotal','entity','purchaseorderdetails',)


    def createtransaction(self,order):
        id = order.id
        subtotal = order.subtotal
        cgst = order.cgst
        sgst = order.sgst
        igst = order.igst
        gtotal = order.gtotal
        pentity = order.entity
        purchaseid = account.objects.get(entity =pentity,accountcode = 1000)
        cgstid = account.objects.get(entity =pentity,accountcode = 6001)
        sgstid = account.objects.get(entity =pentity,accountcode = 6002)
        igstid = account.objects.get(entity =pentity,accountcode = 6003)
        #Transactions.objects.create(account= purchaseid,transactiontype = 'P',transactionid = id,desc = 'Purchase from',drcr=1,amount=subtotal,entity=pentity,createdby = order.createdby )
        StockTransactions.objects.create(accounthead = cgstid.accounthead, account= cgstid,transactiontype = 'P',transactionid = id,desc = 'Purchase',drcr=1,debitamount=cgst,entity=pentity,createdby= order.createdby)
        StockTransactions.objects.create(accounthead = sgstid.accounthead,account= sgstid,transactiontype = 'P',transactionid = id,desc = 'Purchase',drcr=1,debitamount=sgst,entity=pentity,createdby= order.createdby)
        StockTransactions.objects.create(accounthead= order.account.accounthead,account= order.account,transactiontype = 'P',transactionid = id,desc = 'PurchaseBy',drcr=0,creditamount=gtotal,entity=pentity,createdby= order.createdby)
        return id


    def create(self, validated_data):
       # print(validated_data)
        PurchaseOrderDetails_data = validated_data.pop('purchaseorderdetails')
        order = purchaseorder.objects.create(**validated_data)
        pentity = order.entity






        #print(order.objects.get("id"))
        #print(tracks_data)
        for PurchaseOrderDetail_data in PurchaseOrderDetails_data:
            detail = PurchaseOrderDetails.objects.create(purchaseorder = order, **PurchaseOrderDetail_data)
            print(detail)
            if(detail.orderqty ==0.00):
                qty = detail.pieces
            else:
                qty = detail.orderqty
            
            StockTransactions.objects.create(accounthead = detail.product.purchaseaccount.accounthead,account= detail.product.purchaseaccount,stock=detail.product,transactiontype = 'P',transactionid = detail.id,desc = 'Purchase By V.No' + str(order.voucherno),stockttype = 'P',purchasequantity = qty,drcr = 1,debitamount = detail.amount,cgstdr = detail.cgst,sgstdr= detail.sgst,igstdr = detail.igst,entrydate = order.billdate,entity = order.entity,createdby = order.createdby)
            
            


            




          #  StockTransactions.objects.create(stock = detail.product,transactiontype = 'P',transactionid = detail.id,desc = 'Purchase By V.No' + str(order.voucherno),stocktransaction = 'P',quantity = qty,entrydate = order.billdate,entity = order.entity,createdby = order.createdby )

        self.createtransaction(order)
        return order

    def update(self, instance, validated_data):
        fields = ['voucherdate','voucherno','account','billno','billdate','terms','taxtype','billcash','subtotal','cgst','sgst','igst','expenses','gtotal','entity']
        for field in fields:
            try:
                setattr(instance, field, validated_data[field])
            except KeyError:  # validated_data may not contain all fields during HTTP PATCH
                pass
        instance.save()

        items = validated_data.get('purchaseorderdetails')

        product_items_dict = dict((i.id, i) for i in instance.purchaseorderdetails.all())
        print(product_items_dict)

        for item in items:
            item_id = item.get('id', None)
            if item_id:

                product_items_dict.pop(item_id)
                inv_item = PurchaseOrderDetails.objects.get(id=item_id, purchaseorder=instance)
                inv_item.product = item.get('product', inv_item.product)
                inv_item.purchasedesc = item.get('purchasedesc', inv_item.purchasedesc)
                inv_item.orderqty = item.get('orderqty', inv_item.orderqty)
                inv_item.pieces = item.get('pieces', inv_item.pieces)
                inv_item.rate = item.get('rate', inv_item.rate)
                inv_item.amount = item.get('amount', inv_item.amount)
                inv_item.cgst = item.get('cgst', inv_item.cgst)
                inv_item.sgst = item.get('sgst', inv_item.sgst)
                inv_item.igst = item.get('igst', inv_item.igst)
                inv_item.linetotal = item.get('linetotal', inv_item.linetotal)
                inv_item.entity = item.get('entity', inv_item.entity)
                inv_item.save()
            else:
                PurchaseOrderDetails.objects.create(purchaseorder=instance, **item)


        if len(product_items_dict) > 0:
            for item in product_items_dict.values():
                item.delete()
        return instance

    # def get_or_create_packages(self, packages):
    #     package_ids = []
    #     for package in packages:
    #         package_instance, created = PurchaseOrderDetails.objects.get_or_create(pk=package.get('id'), defaults=package)
    #         package_ids.append(package_instance.pk)
    #     return package_ids

    # def create_or_update_packages(self, packages):
    #     package_ids = []
    #     for package in packages:
    #         package_id = package.get('id', None)
    #         print(package_id)

    #         package_instance, created = PurchaseOrderDetails.objects.update_or_create(pk=package.get('id'), defaults=package)
    #         package_ids.append(package_instance.pk)
    #     return package_ids

    # def create(self, validated_data):
    #     package = validated_data.pop('PurchaseOrderDetails', [])
    #     order = purchaseorder.objects.create(**validated_data)
    #     order.purchaseOrder.set(self.get_or_create_packages(package))
    #     return order

    # def update(self, instance, validated_data):
    #     package = validated_data.pop('PurchaseOrderDetails', [])
    #     instance.purchaseOrder.set(self.create_or_update_packages(package))
        # fields = ['VoucherDate','VoucherNo','account','BillNo','BillDate','Terms','TaxType','BillCash','subtotal','Cgst','Sgst','Igst','Expenses','GTotal','entity']
        # for field in fields:
        #     try:
        #         setattr(instance, field, validated_data[field])
        #     except KeyError:  # validated_data may not contain all fields during HTTP PATCH
        #         pass
    #     print(list[instance])
    #     instance.save()
    #     return instance

class journalSerializer(serializers.ModelSerializer):
    #id = serializers.IntegerField(required=False)
    #entityUser = entityUserSerializer(many=True)

    class Meta:
        model = journal
        fields = '__all__'

    def create(self, validated_data):

        # print(validated_data.get('amount'))
        # print('hello')
        order = journal.objects.create(**validated_data)

        if order.drcr == 0:
            creditamount = order.amount
            debitamount = 0
        else:
            debitamount = order.amount
            creditamount = 0



        StockTransactions.objects.create(accounthead= order.account.accounthead,account= order.account,transactiontype = 'J',transactionid = order.id,desc = 'Journal V.No' + str(order.voucherno),drcr=order.drcr,creditamount=creditamount,debitamount=debitamount,entity=order.entity,createdby= order.createdby)
        #Transactions.objects.create(account= Jv.account,transactiontype = 'J',transactionid = Jv.id,desc = 'Journal',drcr=Jv.drcr,amount=Jv.amount,entity=Jv.entity,createdby= Jv.createdby)

        return order



class TrialbalanceSerializer(serializers.ModelSerializer):


  #  purchasequantity1 = serializers.DecimalField(max_digits=10,decimal_places=2)

    accounthead = serializers.IntegerField()
    accountheadname = serializers.CharField(max_length=500,source = 'accounthead__name')
    debit = serializers.DecimalField(max_digits=10,decimal_places=2)
    credit = serializers.DecimalField(max_digits=10,decimal_places=2)
   

    class Meta:
        model = StockTransactions
        fields = ['accounthead','accountheadname','debit','credit']



class TrialbalanceSerializerbyaccounthead(serializers.ModelSerializer):


  #  purchasequantity1 = serializers.DecimalField(max_digits=10,decimal_places=2)

    account = serializers.IntegerField()
    accountname = serializers.CharField(max_length=500,source = 'account__accountname')
    debit = serializers.DecimalField(max_digits=10,decimal_places=2)
    credit = serializers.DecimalField(max_digits=10,decimal_places=2)
   

    class Meta:
        model = StockTransactions
        fields = ['account','accountname','debit','credit']


class stocktranserilaizer(serializers.ModelSerializer):

    # # debit  = serializers.SerializerMethodField()
    # sum_amount = serializers.SerializerMethodField()

    # def get_debit(self, obj):
    #     return obj.debitamount.Count()


    class Meta:
        model = StockTransactions
        fields = ['accounthead','account','transactiontype','debitamount','creditamount']





class accountheadserializer(serializers.ModelSerializer):
    headtrans = stocktranserilaizer(source = 'accounthead_transactions', many=True, read_only=True)

    debit  = serializers.SerializerMethodField()
    credit = serializers.SerializerMethodField()

    class Meta:
        model = accountHead
        fields = ['id','name','debit','credit','headtrans']

    def get_debit(self, obj):
        # fromDate = parse_datetime(self.context['request'].query_params.get(
        #     'fromDate') + ' ' + '00:00:00').strftime('%Y-%m-%d %H:%M:%S')
        # toDate = parse_datetime(self.context['request'].query_params.get(
        #     'toDate') + ' ' + '00:00:00').strftime('%Y-%m-%d %H:%M:%S')
        return obj.headtrans.aggregate(Sum('debitamount'))['debitamount__sum']

    def get_credit(self, obj):
        # fromDate = parse_datetime(self.context['request'].query_params.get(
        #     'fromDate') + ' ' + '00:00:00').strftime('%Y-%m-%d %H:%M:%S')
        # toDate = parse_datetime(self.context['request'].query_params.get(
        #     'toDate') + ' ' + '00:00:00').strftime('%Y-%m-%d %H:%M:%S')
        return obj.headtrans.aggregate(Sum('creditamount'))['creditamount__sum']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
       # print(representation['accounttrans'])
        return representation
        # if representation['is_active'] == True:
            



class accountserializer(serializers.ModelSerializer):
    accounttrans = stocktranserilaizer(source = 'account_transactions', many=True, read_only=True)

    debit  = serializers.SerializerMethodField()
    credit = serializers.SerializerMethodField()

    class Meta:
        model = account
        fields = ['id','accountname','debit','credit', 'accounttrans']

    def get_debit(self, obj):
        # fromDate = parse_datetime(self.context['request'].query_params.get(
        #     'fromDate') + ' ' + '00:00:00').strftime('%Y-%m-%d %H:%M:%S')
        # toDate = parse_datetime(self.context['request'].query_params.get(
        #     'toDate') + ' ' + '00:00:00').strftime('%Y-%m-%d %H:%M:%S')
        return obj.accounttrans.aggregate(Sum('debitamount'))['debitamount__sum']

    def get_credit(self, obj):
        # fromDate = parse_datetime(self.context['request'].query_params.get(
        #     'fromDate') + ' ' + '00:00:00').strftime('%Y-%m-%d %H:%M:%S')
        # toDate = parse_datetime(self.context['request'].query_params.get(
        #     'toDate') + ' ' + '00:00:00').strftime('%Y-%m-%d %H:%M:%S')
        if not obj.accounttrans.aggregate(Sum('creditamount'))['creditamount__sum']:
            return ''
        return obj.accounttrans.aggregate(Sum('creditamount'))['creditamount__sum']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        print(representation)
        if not representation['accounttrans']:
            return None
        return representation

        # print(representation)
        # return representation


class accounthserializer(serializers.ModelSerializer):
    #headtrans = accountserializer(source = 'account_transactions2',many=True, read_only=True)
    #headtrans1 = stocktranserilaizer(source = 'account_transactions',many=True, read_only=True)

    # debit  = serializers.SerializerMethodField()
    # credit = serializers.SerializerMethodField()

    class Meta:
        model = accountHead
        fields = ['name']

    # def get_debit(self, obj):
    #     # fromDate = parse_datetime(self.context['request'].query_params.get(
    #     #     'fromDate') + ' ' + '00:00:00').strftime('%Y-%m-%d %H:%M:%S')
    #     # toDate = parse_datetime(self.context['request'].query_params.get(
    #     #     'toDate') + ' ' + '00:00:00').strftime('%Y-%m-%d %H:%M:%S')
    #     return obj.headtrans.aggregate(Sum('debitamount'))['debitamount__sum']

    # def get_credit(self, obj):
    #     # fromDate = parse_datetime(self.context['request'].query_params.get(
    #     #     'fromDate') + ' ' + '00:00:00').strftime('%Y-%m-%d %H:%M:%S')
    #     # toDate = parse_datetime(self.context['request'].query_params.get(
    #     #     'toDate') + ' ' + '00:00:00').strftime('%Y-%m-%d %H:%M:%S')
    #     return obj.headtrans.aggregate(Sum('creditamount'))['creditamount__sum']
    
     


class TrialbalanceSerializerbyaccount(serializers.ModelSerializer):


  #  purchasequantity1 = serializers.DecimalField(max_digits=10,decimal_places=2)

   # account = serializers.IntegerField()
    accountname = serializers.CharField(max_length=500,source='account__accountname')
    debit = serializers.DecimalField(max_digits=10,decimal_places=2)
    credit = serializers.DecimalField(max_digits=10,decimal_places=2)
    transactiontype = serializers.CharField(max_length=50)
    transactionid = serializers.IntegerField()
    entrydate = serializers.DateField()
    desc = serializers.CharField(max_length=500)
   

    class Meta:
        model = StockTransactions
        fields = ['accountname','transactiontype','transactionid','debit','credit','entrydate','desc']

        def to_representation(self, instance):
            original_representation = super().to_representation(instance)

            print(original_representation)

            representation = {
                
                'detail': original_representation,
            }

            return representation





    


class JournalVSerializer(serializers.ModelSerializer):
    #entityUser = entityUserSerializer(many=True)
  #  id = serializers.IntegerField(required=False)

    newvoucher = serializers.SerializerMethodField()

    def get_newvoucher(self, obj):
        if not obj.voucherno:
            return 1
        else:
            return obj.voucherno + 1

    class Meta:
        model = journal
        fields =  ['newvoucher']


class SRSerializer(serializers.ModelSerializer):
    #entityUser = entityUserSerializer(many=True)
  #  id = serializers.IntegerField(required=False)

    newvoucher = serializers.SerializerMethodField()

    def get_newvoucher(self, obj):
        if not obj.voucherno:
            return 1
        else:
            return obj.voucherno + 1


    class Meta:
        model = salereturn
        fields =  ['newvoucher']




class salesreturnDetailsSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    #entityUser = entityUserSerializer(many=True)

    class Meta:
        model = salereturnDetails
        fields = ('id','product', 'purchasedesc','orderqty','pieces','rate','amount','cgst','sgst','igst','linetotal','entity',)






class salesreturnSerializer(serializers.ModelSerializer):
    salereturndetails = salesreturnDetailsSerializer(many=True)

    class Meta:
        model = salereturn
        fields = ('id','voucherdate','voucherno','account','billno','billdate','terms','taxtype','billcash','subtotal','cgst','sgst','igst','expenses','gtotal','entity','salereturndetails',)

    def createtransaction(self,order):
        id = order.id
        subtotal = order.subtotal
        cgst = order.cgst
        sgst = order.sgst
        igst = order.igst
        gtotal = order.gtotal
        pentity = order.entity
        purchaseid = account.objects.get(entity =pentity,accountcode = 1000)
        cgstid = account.objects.get(entity =pentity,accountcode = 6001)
        sgstid = account.objects.get(entity =pentity,accountcode = 6002)
        igstid = account.objects.get(entity =pentity,accountcode = 6003)
        #Transactions.objects.create(account= purchaseid,transactiontype = 'P',transactionid = id,desc = 'Purchase from',drcr=1,amount=subtotal,entity=pentity,createdby = order.createdby )
        StockTransactions.objects.create(accounthead = cgstid.accounthead, account= cgstid,transactiontype = 'SR',transactionid = id,desc = 'Sale return By V.No' + str(order.voucherno),drcr=1,debitamount=cgst,entity=pentity,createdby= order.createdby)
        StockTransactions.objects.create(accounthead = sgstid.accounthead,account= sgstid,transactiontype = 'SR',transactionid = id,desc = 'Sale return By V.No' + str(order.voucherno),drcr=1,debitamount=sgst,entity=pentity,createdby= order.createdby)
        StockTransactions.objects.create(accounthead= order.account.accounthead,account= order.account,transactiontype = 'SR',transactionid = id,desc = 'Sale return By V.No' + str(order.voucherno),drcr=0,creditamount=gtotal,entity=pentity,createdby= order.createdby)
        return id

    def create(self, validated_data):
        #print(validated_data)
        PurchaseOrderDetails_data = validated_data.pop('salereturndetails')

        print(validated_data.get('account'))
        order = salereturn.objects.create(**validated_data)
        # pk = (salereturn.objects.last()).voucherno
        # print(pk)
        #print(order)
        for PurchaseOrderDetail_data in PurchaseOrderDetails_data:
            #salereturnDetails.objects.create(salereturn = order, test = pk, **PurchaseOrderDetail_data)
            detail = salereturnDetails.objects.create(salereturn = order,**PurchaseOrderDetail_data)
            if(detail.orderqty ==0.00):
                qty = detail.pieces
            else:
                qty = detail.orderqty
            StockTransactions.objects.create(accounthead = detail.product.purchaseaccount.accounthead,account= detail.product.purchaseaccount,stock=detail.product,transactiontype = 'SR',transactionid = detail.id,desc = 'Sale return By V.No' + str(order.voucherno),stockttype = 'P',purchasequantity = qty,drcr = 1,debitamount = detail.amount,cgstdr = detail.cgst,sgstdr= detail.sgst,igstdr = detail.igst,entrydate = order.billdate,entity = order.entity,createdby = order.createdby)
        
        self.createtransaction(order)
        return order

    def update(self, instance, validated_data):
        fields = ['voucherdate','voucherno','account','billno','billdate','terms','taxtype','billcash','subtotal','cgst','sgst','igst','expenses','gtotal','entity']
        for field in fields:
            try:
                setattr(instance, field, validated_data[field])
            except KeyError:  # validated_data may not contain all fields during HTTP PATCH
                pass
        instance.save()

        items = validated_data.get('salereturndetails')

        product_items_dict = dict((i.id, i) for i in instance.salereturndetails.all())
        print(product_items_dict)

        for item in items:
            item_id = item.get('id', None)
            if item_id:

                product_items_dict.pop(item_id)
                inv_item = salereturnDetails.objects.get(id=item_id, salereturn=instance)
                inv_item.product = item.get('product', inv_item.product)
                inv_item.purchasedesc = item.get('purchasedesc', inv_item.purchasedesc)
                inv_item.orderqty = item.get('orderqty', inv_item.orderqty)
                inv_item.pieces = item.get('pieces', inv_item.pieces)
                inv_item.rate = item.get('rate', inv_item.rate)
                inv_item.amount = item.get('amount', inv_item.amount)
                inv_item.cgst = item.get('cgst', inv_item.cgst)
                inv_item.sgst = item.get('sgst', inv_item.sgst)
                inv_item.igst = item.get('igst', inv_item.igst)
                inv_item.linetotal = item.get('linetotal', inv_item.linetotal)
                inv_item.entity = item.get('entity', inv_item.entity)
                inv_item.save()
            else:
                salereturnDetails.objects.create(salereturn=instance, **item)


        if len(product_items_dict) > 0:
            for item in product_items_dict.values():
                item.delete()
        return instance

    # def get_or_create_packages(self, packages):
    #     package_ids = []
    #     for package in packages:
    #         package_instance, created = PurchaseOrderDetails.objects.get_or_create(pk=package.get('id'), defaults=package)
    #         package_ids.append(package_instance.pk)
    #     return package_ids

    # def create_or_update_packages(self, packages):
    #     package_ids = []
    #     for package in packages:
    #         package_id = package.get('id', None)
    #         print(package_id)

    #         package_instance, created = PurchaseOrderDetails.objects.update_or_create(pk=package.get('id'), defaults=package)
    #         package_ids.append(package_instance.pk)
    #     return package_ids

    # def create(self, validated_data):
    #     package = validated_data.pop('PurchaseOrderDetails', [])
    #     order = purchaseorder.objects.create(**validated_data)
    #     order.purchaseOrder.set(self.get_or_create_packages(package))
    #     return order

    # def update(self, instance, validated_data):
    #     package = validated_data.pop('PurchaseOrderDetails', [])
    #     instance.purchaseOrder.set(self.create_or_update_packages(package))
        # fields = ['VoucherDate','VoucherNo','account','BillNo','BillDate','Terms','TaxType','BillCash','subtotal','Cgst','Sgst','Igst','Expenses','GTotal','entity']
        # for field in fields:
        #     try:
        #         setattr(instance, field, validated_data[field])
        #     except KeyError:  # validated_data may not contain all fields during HTTP PATCH
        #         pass
    #     print(list[instance])
    #     instance.save()
    #     return instance









