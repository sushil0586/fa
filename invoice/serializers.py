import imp
from rest_framework import serializers
from invoice.models import SalesOderHeader,salesOrderdetails,purchaseorder,PurchaseOrderDetails



class salesOrderdetailsSerializer(serializers.ModelSerializer):
    #entityUser = entityUserSerializer(many=True)

    class Meta:
        model = salesOrderdetails
        fields = '__all__'


class SalesOderHeaderSerializer(serializers.ModelSerializer):
    salesOrderdetails = salesOrderdetailsSerializer(many=True)

    class Meta:
        model = SalesOderHeader
        fields = '__all__'


class PurchaseOrderDetailsSerializer(serializers.ModelSerializer):
    #entityUser = entityUserSerializer(many=True)

    class Meta:
        model = PurchaseOrderDetails
        fields = ('id','Orderqty','pieces','Rate','Amount','CSGT','SGST','IGST','HSNNo','LineTotal','entity',)


class purchaseorderSerializer(serializers.ModelSerializer):
    PurchaseOrderDetails = PurchaseOrderDetailsSerializer(many=True)

    class Meta:
        model = purchaseorder
        fields = ('VoucherDate','VoucherNo','account','BillNo','BillDate','Terms','TaxType','BillCash','subtotal','Cgst','Sgst','Igst','Expenses','GTotal','entity','PurchaseOrderDetails',)

    def create(self, validated_data):
        #print(validated_data)
        PurchaseOrderDetails_data = validated_data.pop('PurchaseOrderDetails')
        order = purchaseorder.objects.create(**validated_data)
        #print(tracks_data)
        for PurchaseOrderDetail_data in PurchaseOrderDetails_data:
            PurchaseOrderDetails.objects.create(purchaseOrder = order, **PurchaseOrderDetail_data)
        return order



    




