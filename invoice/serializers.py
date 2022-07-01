
import imp
from rest_framework import serializers
from invoice.models import SalesOderHeader,salesOrderdetails,purchaseorder,PurchaseOrderDetails,journal,salereturn,salereturnDetails,Transactions
from financial.models import account



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

    def create(self, validated_data):
        #print(validated_data)
        salesOrderdetails_data = validated_data.pop('salesorderdetails')
        order = SalesOderHeader.objects.create(**validated_data)
        #print(tracks_data)
        for PurchaseOrderDetail_data in salesOrderdetails_data:
            salesOrderdetails.objects.create(salesorderheader = order, **PurchaseOrderDetail_data)
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
        Transactions.objects.create(account= purchaseid,transactiontype = 'P',transactionid = id,desc = 'Purchase from',drcr=1,amount=subtotal,entity=pentity)
        Transactions.objects.create(account= cgstid,transactiontype = 'P',transactionid = id,desc = 'Purchase',drcr=1,amount=cgst,entity=pentity)
        Transactions.objects.create(account= sgstid,transactiontype = 'P',transactionid = id,desc = 'Purchase',drcr=1,amount=sgst,entity=pentity)
        Transactions.objects.create(account= order.account,transactiontype = 'P',transactionid = id,desc = 'PurchaseBy',drcr=0,amount=gtotal,entity=pentity)
        return id


    def create(self, validated_data):
       # print(validated_data)
        PurchaseOrderDetails_data = validated_data.pop('purchaseorderdetails')
        order = purchaseorder.objects.create(**validated_data)


        



        #print(order.objects.get("id"))
        #print(tracks_data)
        for PurchaseOrderDetail_data in PurchaseOrderDetails_data:
            PurchaseOrderDetails.objects.create(purchaseorder = order, **PurchaseOrderDetail_data)

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
            salereturnDetails.objects.create(salereturn = order,**PurchaseOrderDetail_data)
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




    




