
import imp
from itertools import product
from os import device_encoding
from select import select
from rest_framework import serializers
from invoice.models import SalesOderHeader,salesOrderdetails,purchaseorder,PurchaseOrderDetails,\
    journal,salereturn,salereturnDetails,Transactions,StockTransactions,PurchaseReturn,Purchasereturndetails
from financial.models import account,accountHead
from inventory.models import Product
from django.db.models import Sum,Count



class stocktransaction:
    def __init__(self, order,transactiontype,debit,credit,description):
        self.order = order
        self.transactiontype = transactiontype
        self.debit = debit
        self.credit = credit
        self.description = description
    
    def createtransaction(self):
        id = self.order.id
        subtotal = self.order.subtotal
        cgst = self.order.cgst
        sgst = self.order.sgst
        igst = self.order.igst
        gtotal = self.order.gtotal
        pentity = self.order.entity
        purchaseid = account.objects.get(entity =pentity,accountcode = 1000)
        cgstid = account.objects.get(entity =pentity,accountcode = 6001)
        sgstid = account.objects.get(entity =pentity,accountcode = 6002)
        igstid = account.objects.get(entity =pentity,accountcode = 6003)
        #Transactions.objects.create(account= purchaseid,transactiontype = 'P',transactionid = id,desc = 'Purchase from',drcr=1,amount=subtotal,entity=pentity,createdby = order.createdby )
        StockTransactions.objects.create(accounthead = cgstid.accounthead, account= cgstid,transactiontype = self.transactiontype,transactionid = id,desc = self.description,drcr=self.debit,debitamount=cgst,entity=pentity,createdby= self.order.createdby)
        StockTransactions.objects.create(accounthead = sgstid.accounthead,account= sgstid,transactiontype = self.transactiontype,transactionid = id,desc = self.description,drcr=self.debit,debitamount=sgst,entity=pentity,createdby= self.order.createdby)
        StockTransactions.objects.create(accounthead= self.order.account.accounthead,account= self.order.account,transactiontype = self.transactiontype,transactionid = id,desc = self.description,drcr=self.credit,creditamount=gtotal,entity=pentity,createdby= self.order.createdby)
        return id

    def updateransaction(self):
        id = self.order.id
        subtotal = self.order.subtotal
        cgst = self.order.cgst
       
        sgst = self.order.sgst
        igst = self.order.igst
        gtotal = self.order.gtotal
        pentity = self.order.entity
        purchaseid = account.objects.get(entity =pentity,accountcode = 1000)
        cgstid = account.objects.get(entity =pentity,accountcode = 6001)
        #print(cgstid.id)
        sgstid = account.objects.get(entity =pentity,accountcode = 6002)
        igstid = account.objects.get(entity =pentity,accountcode = 6003)

        #print(self.order.id)

        #print(StockTransactions.objects.filter(transactionid = self.order.id,transactiontype = 'P'))
        StockTransactions.objects.filter(transactionid = self.order.id,transactiontype = self.transactiontype,account = self.order.account).update(accounthead= self.order.account.accounthead,account= self.order.account,transactiontype = self.transactiontype,desc = self.description,drcr=self.credit,creditamount=gtotal,entity=pentity,createdby= self.order.createdby)
       # StockTransactions.objects.filter(transactionid = self.order.id,transactiontype = 'P',account = self.order.account).update(accounthead= self.order.account.accounthead,account= self.order.account,transactiontype = self.transactiontype,desc = self.description,drcr=self.credit,creditamount=gtotal,entity=pentity,createdby= self.order.createdby)
        #Transactions.objects.create(account= purchaseid,transactiontype = 'P',transactionid = id,desc = 'Purchase from',drcr=1,amount=subtotal,entity=pentity,createdby = order.createdby )
        StockTransactions.objects.filter(transactionid = self.order.id,transactiontype = self.transactiontype,account_id = cgstid.id).update(accounthead = cgstid.accounthead, account= cgstid,transactiontype = self.transactiontype,transactionid = id,desc = self.description,drcr=self.debit,debitamount=cgst,entity=pentity,createdby= self.order.createdby)
        StockTransactions.objects.filter(transactionid = self.order.id,transactiontype = self.transactiontype,account_id = sgstid.id).update(accounthead = sgstid.accounthead,account= sgstid,transactiontype = self.transactiontype,transactionid = id,desc = self.description,drcr=self.debit,debitamount=sgst,entity=pentity,createdby= self.order.createdby)
        
        return id


    def createtransactiondetails(self,detail,stocktype):

        if (detail.orderqty ==0.00):
                qty = detail.pieces
        else:
                qty = detail.orderqty

        details = StockTransactions.objects.create(accounthead = detail.product.purchaseaccount.accounthead,account= detail.product.purchaseaccount,stock=detail.product,transactiontype = self.transactiontype,transactionid = self.order.id,desc = 'Purchase By V.No' + str(self.order.voucherno),stockttype = stocktype,purchasequantity = qty,drcr = self.debit,debitamount = detail.amount,cgstdr = detail.cgst,sgstdr= detail.sgst,igstdr = detail.igst,entrydate = self.order.billdate,entity = self.order.entity,createdby = self.order.createdby)

        return details

    def updatetranasationdetails(self,updateddetails,stocktype):
        if (updateddetails.orderqty ==0.00):
                qty = updateddetails.pieces
        else:
                qty = updateddetails.orderqty

        details = StockTransactions.objects.filter(transactionid = self.order.id,transactiontype = self.transactiontype,account_id = updateddetails.product.purchaseaccount.id).create(accounthead = updateddetails.product.purchaseaccount.accounthead,account= updateddetails.product.purchaseaccount,stock=updateddetails.product,transactiontype = self.transactiontype,transactionid = self.order.id,desc = 'Purchase By V.No' + str(self.order.voucherno),stockttype = stocktype,purchasequantity = qty,drcr = self.debit,debitamount = updateddetails.amount,cgstdr = updateddetails.cgst,sgstdr= updateddetails.sgst,igstdr = updateddetails.igst,entrydate = self.order.billdate,entity = self.order.entity,createdby = self.order.createdby)
        #details = StockTransactions.objects.filter(transactionid = instance.id,transactiontype = 'P',account_id = inv_item.product.purchaseaccount.id).create(accounthead = inv_item.product.purchaseaccount.accounthead,account= inv_item.product.purchaseaccount,stock=inv_item.product,transactiontype = 'P',transactionid = inv_item.id,desc = 'Purchase By V.No',stockttype = 'P',purchasequantity = qty,drcr = 1,debitamount = inv_item.amount,cgstdr = inv_item.cgst,sgstdr= inv_item.sgst,igstdr = inv_item.igst,entrydate = instance.billdate,entity = instance.entity,createdby = instance.createdby)

        return details



class stocktransactionsale:
    def __init__(self, order,transactiontype,debit,credit,description):
        self.order = order
        self.transactiontype = transactiontype
        self.debit = debit
        self.credit = credit
        self.description = description
    
    def createtransaction(self):
        id = self.order.id
        subtotal = self.order.subtotal
        cgst = self.order.cgst
        sgst = self.order.sgst
        igst = self.order.igst
        gtotal = self.order.gtotal
        pentity = self.order.entity
        purchaseid = account.objects.get(entity =pentity,accountcode = 3000)
        cgstid = account.objects.get(entity =pentity,accountcode = 6001)
        sgstid = account.objects.get(entity =pentity,accountcode = 6002)
        igstid = account.objects.get(entity =pentity,accountcode = 6003)
        StockTransactions.objects.create(accounthead = cgstid.accounthead, account= cgstid,transactiontype = self.transactiontype,transactionid = id,desc = self.description + ' ' + str(self.order.billno),drcr=self.credit,creditamount=cgst,entity=self.order.entity,createdby= self.order.owner)
        StockTransactions.objects.create(accounthead = sgstid.accounthead,account= sgstid,transactiontype = self.transactiontype,transactionid = id,desc = self.description + ' ' + str(self.order.billno),drcr=self.credit,creditamount=sgst,entity=self.order.entity,createdby= self.order.owner)
        StockTransactions.objects.create(accounthead= self.order.accountid.accounthead,account= self.order.accountid,transactiontype = self.transactiontype,transactionid = id,desc = self.description + ' ' + str(self.order.billno),drcr=self.debit,debitamount=gtotal,entity=self.order.entity,createdby= self.order.owner)
        return id

    def updateransaction(self):

        id = self.order.id
        subtotal = self.order.subtotal
        cgst = self.order.cgst
        sgst = self.order.sgst
        igst = self.order.igst
        gtotal = self.order.gtotal
        pentity = self.order.entity
        purchaseid = account.objects.get(entity =pentity,accountcode = 3000)
        cgstid = account.objects.get(entity =pentity,accountcode = 6001)
        sgstid = account.objects.get(entity =pentity,accountcode = 6002)
        igstid = account.objects.get(entity =pentity,accountcode = 6003)
        StockTransactions.objects.filter(transactionid = self.order.id,transactiontype = self.transactiontype,account_id = cgstid.id).create(accounthead = cgstid.accounthead, account= cgstid,transactiontype = self.transactiontype,transactionid = id,desc = self.description + ' ' + str(self.order.billno),drcr=self.credit,creditamount=cgst,entity=self.order.entity,createdby= self.order.owner)
        StockTransactions.objects.filter(transactionid = self.order.id,transactiontype = self.transactiontype,account_id = sgstid.id).create(accounthead = sgstid.accounthead,account= sgstid,transactiontype = self.transactiontype,transactionid = id,desc = self.description + ' ' + str(self.order.billno),drcr=self.credit,creditamount=sgst,entity=self.order.entity,createdby= self.order.owner)
        StockTransactions.objects.filter(transactionid = self.order.id,transactiontype = self.transactiontype,account = self.order.accountid).update(accounthead= self.order.accountid.accounthead,account= self.order.accountid,transactiontype = self.transactiontype,transactionid = id,desc = self.description + ' ' + str(self.order.billno),drcr=self.debit,debitamount=gtotal,entity=self.order.entity,createdby= self.order.owner)
        
        return id


    def createtransactiondetails(self,detail,stocktype):

        if (detail.orderqty ==0.00):
                qty = detail.pieces
        else:
                qty = detail.orderqty

        details = StockTransactions.objects.create(accounthead = detail.product.saleaccount.accounthead,account= detail.product.saleaccount,stock=detail.product,transactiontype = self.transactiontype,transactionid = self.order.id,desc = self.description + ' ' + str(self.order.voucherno),stockttype = stocktype,purchasequantity = qty,drcr = self.debit,debitamount = detail.amount,cgstdr = detail.cgst,sgstdr= detail.sgst,igstdr = detail.igst,entrydate = self.order.billdate,entity = self.order.entity,createdby = self.order.createdby)

        return details

    def updatetranasationdetails(self,updateddetails,stocktype):
        if (updateddetails.orderqty ==0.00):
                qty = updateddetails.pieces
        else:
                qty = updateddetails.orderqty

        details = StockTransactions.objects.filter(transactionid = self.order.id,transactiontype = self.transactiontype,account_id = updateddetails.product.saleaccount.id).create(accounthead = updateddetails.product.saleaccount.accounthead,account= updateddetails.product.saleaccount,stock=updateddetails.product,transactiontype = self.transactiontype,transactionid = self.order.id,desc = 'Purchase By V.No' + str(self.order.voucherno),stockttype = stocktype,purchasequantity = qty,drcr = self.debit,debitamount = updateddetails.amount,cgstdr = updateddetails.cgst,sgstdr= updateddetails.sgst,igstdr = updateddetails.igst,entrydate = self.order.billdate,entity = self.order.entity,createdby = self.order.createdby)
        #details = StockTransactions.objects.filter(transactionid = instance.id,transactiontype = 'P',account_id = inv_item.product.purchaseaccount.id).create(accounthead = inv_item.product.purchaseaccount.accounthead,account= inv_item.product.purchaseaccount,stock=inv_item.product,transactiontype = 'P',transactionid = inv_item.id,desc = 'Purchase By V.No',stockttype = 'P',purchasequantity = qty,drcr = 1,debitamount = inv_item.amount,cgstdr = inv_item.cgst,sgstdr= inv_item.sgst,igstdr = inv_item.igst,entrydate = instance.billdate,entity = instance.entity,createdby = instance.createdby)

        return details




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
        stk = stocktransactionsale(order, transactiontype= 'S',debit=1,credit=0,description= 'Sale ')
        #print(tracks_data)
        for PurchaseOrderDetail_data in salesOrderdetails_data:
            detail = salesOrderdetails.objects.create(salesorderheader = order, **PurchaseOrderDetail_data)
            stk.createtransactiondetails(detail=detail,stocktype='S')

            # if(detail.orderqty ==0.00):
            #     qty = detail.pieces
            # else:
            #     qty = detail.orderqty
            # StockTransactions.objects.create(accounthead = detail.product.saleaccount.accounthead,account= detail.product.saleaccount,stock=detail.product,transactiontype = 'S',transactionid = order.id,desc = 'Sale By B.No ' + str(order.billno),stockttype = 'S',salequantity = qty,drcr = 0,creditamount = detail.amount,cgstcr = detail.cgst,sgstcr= detail.sgst,igstcr = detail.igst,entrydate = order.sorderdate,entity = order.entity,createdby = order.owner)

        stk.createtransaction()
        return order

    def update(self, instance, validated_data):
        fields = ['sorderdate','billno','accountid','latepaymentalert','grno','vehicle','taxtype','billcash','supply','shippedto','remarks','transport','broker','tds194q','tcs206c1ch1','tcs206c1ch2','tcs206c1ch3','tcs206C1','tcs206C2','duedate','subtotal','subtotal','cgst','sgst','igst','expenses','gtotal','entity','owner',]
        for field in fields:
            try:
                setattr(instance, field, validated_data[field])
            except KeyError:  # validated_data may not contain all fields during HTTP PATCH
                pass
        instance.save()
        stk = stocktransactionsale(instance, transactiontype= 'S',debit=1,credit=0,description= 'Sale')
        stk.updateransaction()

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
                stk.updatetranasationdetails(updateddetails= inv_item,stocktype='S')
            else:
                detail = salesOrderdetails.objects.create(salesorderheader=instance, **item)
                stk.createtransactiondetails(detail= detail,stocktype='S')


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


    def create(self, validated_data):
        #print(validated_data)
        salesOrderdetails_data = validated_data.pop('purchasereturndetails')
        order = PurchaseReturn.objects.create(**validated_data)
        stk = stocktransactionsale(order, transactiontype= 'SR',debit=1,credit=0,description= 'Purchase Return')
        #print(tracks_data)
        for PurchaseOrderDetail_data in salesOrderdetails_data:
            detail = Purchasereturndetails.objects.create(purchasereturn = order, **PurchaseOrderDetail_data)
            stk.createtransactiondetails(detail=detail,stocktype='PR')

            

        stk.createtransaction()
        return order

    def update(self, instance, validated_data):
        fields = ['sorderdate','billno','accountid','latepaymentalert','grno','vehicle','taxtype','billcash','supply','shippedto','remarks','transport','broker','tds194q','tcs206c1ch1','tcs206c1ch2','tcs206c1ch3','tcs206C1','tcs206C2','duedate','subtotal','subtotal','cgst','sgst','igst','expenses','gtotal','entity','owner',]
        for field in fields:
            try:
                setattr(instance, field, validated_data[field])
            except KeyError:  # validated_data may not contain all fields during HTTP PATCH
                pass
        instance.save()
        stk = stocktransactionsale(instance, transactiontype= 'PR',debit=1,credit=0,description= 'Purchase Return')
        stk.updateransaction()

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
                stk.updatetranasationdetails(updateddetails= inv_item,stocktype='PR')
            else:
                detail = Purchasereturndetails.objects.create(purchasereturn=instance, **item)
                stk.createtransactiondetails(detail= detail,stocktype='PR')


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
    productname = serializers.SerializerMethodField()
   # productdesc1 = serializers.SerializerMethodField()
    #entityUser = entityUserSerializer(many=True)

    class Meta:
        model = PurchaseOrderDetails
        fields = ('id','product','productname','purchasedesc','orderqty','pieces','rate','amount','cgst','sgst','igst','linetotal','entity',)
    
    def get_productname(self,obj):
        return obj.product.productname







class purchaseorderSerializer(serializers.ModelSerializer):
    purchaseorderdetails = PurchaseOrderDetailsSerializer(many=True)
   # productname = serializers.SerializerMethodField()

    class Meta:
        model = purchaseorder
        fields = ('id','voucherdate','voucherno','account','billno','billdate','terms','taxtype','billcash','subtotal','cgst','sgst','igst','expenses','gtotal','entity','purchaseorderdetails',)


    
    


    def create(self, validated_data):
       # print(validated_data)
        PurchaseOrderDetails_data = validated_data.pop('purchaseorderdetails')
        order = purchaseorder.objects.create(**validated_data)
        stk = stocktransaction(order, transactiontype= 'P',debit=1,credit=0,description= 'Purchase')
        #print(order.objects.get("id"))
        #print(tracks_data)
        for PurchaseOrderDetail_data in PurchaseOrderDetails_data:
            detail = PurchaseOrderDetails.objects.create(purchaseorder = order, **PurchaseOrderDetail_data)
          
            stk.createtransactiondetails(detail=detail,stocktype='P')
            
        
        stk.createtransaction()
        return order

    def update(self, instance, validated_data):
        fields = ['voucherdate','voucherno','account','billno','billdate','terms','taxtype','billcash','subtotal','cgst','sgst','igst','expenses','gtotal','entity']
        for field in fields:
            try:
                setattr(instance, field, validated_data[field])
            except KeyError:  # validated_data may not contain all fields during HTTP PATCH
                pass
        

        # print(instance.id)
        stk = stocktransaction(instance, transactiontype= 'P',debit=1,credit=0,description= 'updated')
        stk.updateransaction()
        
        i = instance.save()

        PurchaseOrderDetails.objects.filter(purchaseorder=instance,entity = instance.entity).delete()
       
        PurchaseOrderDetails_data = validated_data.get('purchaseorderdetails')

        for PurchaseOrderDetail_data in PurchaseOrderDetails_data:
            detail = PurchaseOrderDetails.objects.create(purchaseorder = instance, **PurchaseOrderDetail_data)
            stk.createtransactiondetails(detail=detail,stocktype='P')




        # product_items_dict = dict((i.id, i) for i in instance.purchaseorderdetails.all())
        # #print(product_items_dict)

        # for item in items:
        #     item_id = item.get('id', None)
        #     if item_id:

        #         product_items_dict.pop(item_id)
        #         inv_item = PurchaseOrderDetails.objects.get(id=item_id, purchaseorder=instance)
        #         inv_item.product = item.get('product', inv_item.product)
        #         inv_item.purchasedesc = item.get('purchasedesc', inv_item.purchasedesc)
        #         inv_item.orderqty = item.get('orderqty', inv_item.orderqty)
        #         inv_item.pieces = item.get('pieces', inv_item.pieces)
        #         inv_item.rate = item.get('rate', inv_item.rate)
        #         inv_item.amount = item.get('amount', inv_item.amount)
        #         inv_item.cgst = item.get('cgst', inv_item.cgst)
        #         inv_item.sgst = item.get('sgst', inv_item.sgst)
        #         inv_item.igst = item.get('igst', inv_item.igst)
        #         inv_item.linetotal = item.get('linetotal', inv_item.linetotal)
        #         inv_item.entity = item.get('entity', inv_item.entity)
        #         inv_item.save()
        #         stk.updatetranasationdetails(updateddetails= inv_item,stocktype='P')


                

        #     else:
        #         detail = PurchaseOrderDetails.objects.create(purchaseorder=instance, **item)
        #         stk.createtransactiondetails(detail= detail,stocktype='P')


        # if len(product_items_dict) > 0:
        #     for item in product_items_dict.values():
        #         item.delete()
        return instance


class journalSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = journal
        fields = '__all__'

    def create(self, validated_data):
        order = journal.objects.create(**validated_data)
        if order.drcr == 0:
            creditamount = order.amount
            debitamount = 0
        else:
            debitamount = order.amount
            creditamount = 0
        StockTransactions.objects.create(accounthead= order.account.accounthead,account= order.account,transactiontype = order.vouchertype,transactionid = order.id,desc = 'Journal V.No' + str(order.voucherno),drcr=order.drcr,creditamount=creditamount,debitamount=debitamount,entity=order.entity,createdby= order.createdby)
        return order
    
    # def update(self,instance,validated_data):
    #     instance.save()
    #     StockTransactions.objects.filter(transactiontype = instance.vouchertype,account = instance.account,)

    #     pass



class TrialbalanceSerializer(serializers.ModelSerializer):


  #  purchasequantity1 = serializers.DecimalField(max_digits=10,decimal_places=2)

    accounthead = serializers.IntegerField(source = 'account__accounthead')
    accountheadname = serializers.CharField(max_length=500,source = 'account__accounthead__name')
    debit = serializers.DecimalField(max_digits=10,decimal_places=2)
    credit = serializers.DecimalField(max_digits=10,decimal_places=2)

    #debit  = serializers.SerializerMethodField()
   

    class Meta:
        model = StockTransactions
        fields = ['accounthead','accountheadname','debit','credit']

    

  

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        if representation['debit'] and representation['credit']:
            if float(representation['debit']) - float(representation['credit']) > 0:
                representation['debit'] = float(representation['debit']) - float(representation['credit'])
                representation['credit'] = ''
                return representation
            else:
                representation['credit'] = float(representation['credit']) - float(representation['debit'])
                representation['debit'] = ' '
                return representation
        return representation



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
        fields = ['accounthead','account','transactiontype','debitamount','creditamount','entrydate']





class cashserializer(serializers.ModelSerializer):


    stk = stocktranserilaizer(many=True, read_only=True)
    select_related_fields = ('accounthead')

    # debit  = serializers.SerializerMethodField()
    # credit = serializers.SerializerMethodField()

    class Meta:
        model = accountHead
        fields = ['name','stk']

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

    def to_representation(self, instance):
        representation = super().to_representation(instance)
       # print(representation['accounttrans'])
        return representation
        # if representation['is_active'] == True:





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
  #  dateentry = serializers.SerializerMethodField()

    class Meta:
        model = account
        fields = ['id','accountname','debit','credit', 'accounttrans']
        
    
    def get_dateentry(self, obj):

        print(obj)
        # fromDate = parse_datetime(self.context['request'].query_params.get(
        #     'fromDate') + ' ' + '00:00:00').strftime('%Y-%m-%d %H:%M:%S')
        # toDate = parse_datetime(self.context['request'].query_params.get(
        #     'toDate') + ' ' + '00:00:00').strftime('%Y-%m-%d %H:%M:%S')
       # aggregate(Sum('debitamount'))['debitamount__sum']
        return obj.accounttrans.values('entrydate').annotate(debit = Sum('debitamount'),credit = Sum('creditamount') )


    def get_debit(self, obj):

        print(obj)
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

 
    def create(self, validated_data):
        #print(validated_data)
        PurchaseOrderDetails_data = validated_data.pop('salereturndetails')

        print(validated_data.get('account'))
        order = salereturn.objects.create(**validated_data)
        stk = stocktransaction(order, transactiontype= 'SR',debit=1,credit=0,description= 'Sale Return')
        for PurchaseOrderDetail_data in PurchaseOrderDetails_data:
            
            detail = salereturnDetails.objects.create(salereturn = order,**PurchaseOrderDetail_data)
            stk.createtransactiondetails(detail=detail,stocktype='SR')
           
        
        stk.createtransaction()
        return order

    def update(self, instance, validated_data):
        fields = ['voucherdate','voucherno','account','billno','billdate','terms','taxtype','billcash','subtotal','cgst','sgst','igst','expenses','gtotal','entity']
        for field in fields:
            try:
                setattr(instance, field, validated_data[field])
            except KeyError:  # validated_data may not contain all fields during HTTP PATCH
                pass
        print(instance)
        stk = stocktransaction(instance, transactiontype= 'P',debit=1,credit=0,description= 'updated')
        stk.updateransaction()
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
                stk.updatetranasationdetails(updateddetails= inv_item,stocktype='P')
            else:
                detail = salereturnDetails.objects.create(salereturn=instance, **item)
                stk.createtransactiondetails(detail= detail,stocktype='P')


        if len(product_items_dict) > 0:
            for item in product_items_dict.values():
                item.delete()
        return instance

  








