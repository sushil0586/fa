import imp
from rest_framework import serializers
from invoice.models import SalesOderHeader,salesOrderdetails,purchaseorder,PurchaseOrderDetails



class salesOrderdetailsSerializer(serializers.ModelSerializer):
    #entityUser = entityUserSerializer(many=True)
    id = serializers.IntegerField(required=False)

    class Meta:
        model = salesOrderdetails
        fields =  ('id','product','Orderqty','UnitPrice','discountPercent','discountAmount','LineTotal','owner',)


class SalesOderHeaderSerializer(serializers.ModelSerializer):
    salesOrderdetails = salesOrderdetailsSerializer(many=True)

    class Meta:
        model = SalesOderHeader
        fields = ('id','Sorderdate','Duedate','Shipdate','Staus','SalesOrderNumber','account','subtotal','Taxamount','Freight','TotalAmount','entity','owner','salesOrderdetails',)

    def create(self, validated_data):
        #print(validated_data)
        salesOrderdetails_data = validated_data.pop('salesOrderdetails')
        order = SalesOderHeader.objects.create(**validated_data)
        #print(tracks_data)
        for PurchaseOrderDetail_data in salesOrderdetails_data:
            salesOrderdetails.objects.create(salesOrderHeader = order, **PurchaseOrderDetail_data)
        return order

    def update(self, instance, validated_data):  
        fields = ['Sorderdate','Duedate','Shipdate','Staus','SalesOrderNumber','account','subtotal','Taxamount','Freight','TotalAmount','entity','owner',]
        for field in fields:
            try:
                setattr(instance, field, validated_data[field])
            except KeyError:  # validated_data may not contain all fields during HTTP PATCH
                pass
        instance.save()

        items = validated_data.get('salesOrderdetails')

        product_items_dict = dict((i.id, i) for i in instance.salesOrderdetails.all())
        print(product_items_dict)

        for item in items:
            item_id = item.get('id', None)
            if item_id:



                product_items_dict.pop(item_id)
                inv_item = salesOrderdetails.objects.get(id=item_id, salesOrderHeader=instance)
                inv_item.product = item.get('product', inv_item.product)
                inv_item.Orderqty = item.get('Orderqty', inv_item.Orderqty)
                inv_item.UnitPrice = item.get('UnitPrice', inv_item.UnitPrice)
                inv_item.discountPercent = item.get('discountPercent', inv_item.discountPercent)
                inv_item.discountAmount = item.get('discountAmount', inv_item.discountAmount)
                inv_item.LineTotal = item.get('LineTotal', inv_item.LineTotal)
                inv_item.owner = item.get('owner', inv_item.owner)
                inv_item.save()
            else:
                salesOrderdetails.objects.create(salesOrderHeader=instance, **item)

        
        if len(product_items_dict) > 0:
            for item in product_items_dict.values():
                item.delete()
        return instance



class POSerializer(serializers.ModelSerializer):
    #entityUser = entityUserSerializer(many=True)
  #  id = serializers.IntegerField(required=False)

    Newvoucher = serializers.SerializerMethodField()

    def get_Newvoucher(self, obj):
        return obj.VoucherNo + 1
        

    class Meta:
        model = purchaseorder
        fields =  ['VoucherNo','Newvoucher']




class PurchaseOrderDetailsSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    #entityUser = entityUserSerializer(many=True)

    class Meta:
        model = PurchaseOrderDetails
        fields = ('id','product','Orderqty','pieces','Rate','Amount','CSGT','SGST','IGST','HSNNo','LineTotal','entity',)

    

    


class purchaseorderSerializer(serializers.ModelSerializer):
    PurchaseOrderDetails = PurchaseOrderDetailsSerializer(many=True)

    class Meta:
        model = purchaseorder
        fields = ('id','VoucherDate','VoucherNo','account','BillNo','BillDate','Terms','TaxType','BillCash','subtotal','Cgst','Sgst','Igst','Expenses','GTotal','entity','PurchaseOrderDetails',)

    def create(self, validated_data):
        #print(validated_data)
        PurchaseOrderDetails_data = validated_data.pop('PurchaseOrderDetails')
        order = purchaseorder.objects.create(**validated_data)
        #print(tracks_data)
        for PurchaseOrderDetail_data in PurchaseOrderDetails_data:
            PurchaseOrderDetails.objects.create(purchaseOrder = order, **PurchaseOrderDetail_data)
        return order

    def update(self, instance, validated_data):  
        fields = ['VoucherDate','VoucherNo','account','BillNo','BillDate','Terms','TaxType','BillCash','subtotal','Cgst','Sgst','Igst','Expenses','GTotal','entity']
        for field in fields:
            try:
                setattr(instance, field, validated_data[field])
            except KeyError:  # validated_data may not contain all fields during HTTP PATCH
                pass
        instance.save()

        items = validated_data.get('PurchaseOrderDetails')

        product_items_dict = dict((i.id, i) for i in instance.PurchaseOrderDetails.all())
        print(product_items_dict)

        for item in items:
            item_id = item.get('id', None)
            if item_id:

                product_items_dict.pop(item_id)
                inv_item = PurchaseOrderDetails.objects.get(id=item_id, purchaseOrder=instance)
                inv_item.product = item.get('product', inv_item.product)
                inv_item.Orderqty = item.get('Orderqty', inv_item.Orderqty)
                inv_item.pieces = item.get('pieces', inv_item.pieces)
                inv_item.Rate = item.get('Rate', inv_item.Rate)
                inv_item.Amount = item.get('Amount', inv_item.Amount)
                inv_item.CSGT = item.get('CSGT', inv_item.CSGT)
                inv_item.SGST = item.get('SGST', inv_item.SGST)
                inv_item.IGST = item.get('IGST', inv_item.IGST)
                inv_item.HSNNo = item.get('HSNNo', inv_item.HSNNo)
                inv_item.LineTotal = item.get('LineTotal', inv_item.LineTotal)
                inv_item.entity = item.get('entity', inv_item.entity)
                inv_item.save()
            else:
                PurchaseOrderDetails.objects.create(purchaseOrder=instance, **item)

        
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



    




