
import imp
from itertools import product
from os import device_encoding
from select import select
from rest_framework import serializers
from invoice.models import SalesOderHeader,salesOrderdetails,purchaseorder,PurchaseOrderDetails,\
    journal,salereturn,salereturnDetails,Transactions,StockTransactions,PurchaseReturn,Purchasereturndetails,journalmain,journaldetails,entry,goodstransaction,stockdetails,stockmain
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
        entryid,created  = entry.objects.get_or_create(entrydate1 = self.order.billdate)
        #Transactions.objects.create(account= purchaseid,transactiontype = 'P',transactionid = id,desc = 'Purchase from',drcr=1,amount=subtotal,entity=pentity,createdby = order.createdby )
        StockTransactions.objects.create(accounthead = cgstid.accounthead, account= cgstid,transactiontype = self.transactiontype,transactionid = id,desc = self.description,drcr=self.debit,debitamount=cgst,entity=pentity,createdby= self.order.createdby,entry =entryid,entrydatetime = self.order.billdate)
        StockTransactions.objects.create(accounthead = sgstid.accounthead,account= sgstid,transactiontype = self.transactiontype,transactionid = id,desc = self.description,drcr=self.debit,debitamount=sgst,entity=pentity,createdby= self.order.createdby,entry =entryid,entrydatetime = self.order.billdate)
        StockTransactions.objects.create(accounthead= self.order.account.accounthead,account= self.order.account,transactiontype = self.transactiontype,transactionid = id,desc = self.description,drcr=self.credit,creditamount=gtotal,entity=pentity,createdby= self.order.createdby,entry =entryid,entrydatetime = self.order.billdate)
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
        entryid,created  = entry.objects.get_or_create(entrydate1 = self.order.billdate)

        if self.transactiontype == 'P':
            StockTransactions.objects.filter(entity = pentity,stockttype = 'P',transactionid= id).delete()
            goodstransaction.objects.filter(entity = pentity,stockttype = 'P',transactionid= id).delete()
        
        if self.transactiontype == 'SR':
            StockTransactions.objects.filter(entity = pentity,stockttype = 'SR',transactionid= id).delete()
            goodstransaction.objects.filter(entity = pentity,stockttype = 'SR',transactionid= id).delete()

        #print(self.order.id)

        #print(StockTransactions.objects.filter(transactionid = self.order.id,transactiontype = 'P'))
        StockTransactions.objects.filter(transactionid = self.order.id,transactiontype = self.transactiontype,account = self.order.account,entity = pentity).update(accounthead= self.order.account.accounthead,account= self.order.account,transactiontype = self.transactiontype,desc = self.description,drcr=self.credit,creditamount=gtotal,entity=pentity,createdby= self.order.createdby,entry =entryid,entrydatetime = self.order.billdate)
       # StockTransactions.objects.filter(transactionid = self.order.id,transactiontype = 'P',account = self.order.account).update(accounthead= self.order.account.accounthead,account= self.order.account,transactiontype = self.transactiontype,desc = self.description,drcr=self.credit,creditamount=gtotal,entity=pentity,createdby= self.order.createdby)
        #Transactions.objects.create(account= purchaseid,transactiontype = 'P',transactionid = id,desc = 'Purchase from',drcr=1,amount=subtotal,entity=pentity,createdby = order.createdby )
        StockTransactions.objects.filter(transactionid = self.order.id,transactiontype = self.transactiontype,account_id = cgstid.id,entity = pentity).update(accounthead = cgstid.accounthead, account= cgstid,transactiontype = self.transactiontype,transactionid = id,desc = self.description,drcr=self.debit,debitamount=cgst,entity=pentity,createdby= self.order.createdby,entry =entryid,entrydatetime = self.order.billdate)
        StockTransactions.objects.filter(transactionid = self.order.id,transactiontype = self.transactiontype,account_id = sgstid.id,entity = pentity).update(accounthead = sgstid.accounthead,account= sgstid,transactiontype = self.transactiontype,transactionid = id,desc = self.description,drcr=self.debit,debitamount=sgst,entity=pentity,createdby= self.order.createdby,entry =entryid,entrydatetime = self.order.billdate)
        
        return id


    def createtransactiondetails(self,detail,stocktype):

        if (detail.orderqty ==0.00):
                qty = detail.pieces
        else:
                qty = detail.orderqty

        entryid,created  = entry.objects.get_or_create(entrydate1 = self.order.billdate)

        details = StockTransactions.objects.create(accounthead = detail.product.purchaseaccount.accounthead,account= detail.product.purchaseaccount,stock=detail.product,transactiontype = self.transactiontype,transactionid = self.order.id,desc = 'Purchase By V.No' + str(self.order.voucherno),stockttype = stocktype,purchasequantity = qty,drcr = self.debit,debitamount = detail.amount,cgstdr = detail.cgst,sgstdr= detail.sgst,igstdr = detail.igst,entrydate = self.order.billdate,entity = self.order.entity,createdby = self.order.createdby,entry = entryid,entrydatetime = self.order.billdate)
        goodstransaction.objects.create(account= detail.product.purchaseaccount,stock=detail.product,transactiontype = self.transactiontype,transactionid = self.order.id,stockttype = stocktype,purchasequantity = qty,entrydatetime = self.order.billdate,entity = self.order.entity,createdby = self.order.createdby,entry = entryid)


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
        entryid,created  = entry.objects.get_or_create(entrydate1 = self.order.sorderdate)
        StockTransactions.objects.create(accounthead = cgstid.accounthead, account= cgstid,transactiontype = self.transactiontype,transactionid = id,desc = self.description + ' ' + str(self.order.billno),drcr=self.credit,creditamount=cgst,entity=self.order.entity,createdby= self.order.owner,entry = entryid,entrydatetime = self.order.sorderdate)
        StockTransactions.objects.create(accounthead = sgstid.accounthead,account= sgstid,transactiontype = self.transactiontype,transactionid = id,desc = self.description + ' ' + str(self.order.billno),drcr=self.credit,creditamount=sgst,entity=self.order.entity,createdby= self.order.owner,entry = entryid,entrydatetime = self.order.sorderdate)
        StockTransactions.objects.create(accounthead= self.order.accountid.accounthead,account= self.order.accountid,transactiontype = self.transactiontype,transactionid = id,desc = self.description + ' ' + str(self.order.billno),drcr=self.debit,debitamount=gtotal,entity=self.order.entity,createdby= self.order.owner,entry = entryid,entrydatetime = self.order.sorderdate)
        return id

    def updateransaction(self):

        id = self.order.id
        subtotal = self.order.subtotal
        cgst = self.order.cgst
        sgst = self.order.sgst
        igst = self.order.igst
        gtotal = self.order.gtotal
        pentity = self.order.entity
        if self.transactiontype == 'S':
            StockTransactions.objects.filter(entity = pentity,stockttype = 'S',transactionid= id).delete()
            goodstransaction.objects.filter(entity = pentity,stockttype = 'S',transactionid= id).delete()
        
        if self.transactiontype == 'PR':
            StockTransactions.objects.filter(entity = pentity,stockttype = 'PR',transactionid= id).delete()
            goodstransaction.objects.filter(entity = pentity,stockttype = 'PR',transactionid= id).delete()
        purchaseid = account.objects.get(entity =pentity,accountcode = 3000)
        cgstid = account.objects.get(entity =pentity,accountcode = 6001)
        sgstid = account.objects.get(entity =pentity,accountcode = 6002)
        igstid = account.objects.get(entity =pentity,accountcode = 6003)
        entryid,created  = entry.objects.get_or_create(entrydate1 = self.order.sorderdate)
        StockTransactions.objects.filter(transactionid = self.order.id,transactiontype = self.transactiontype,account = cgstid,entity = pentity).update(accounthead = cgstid.accounthead, account= cgstid,transactiontype = self.transactiontype,transactionid = id,desc = self.description + ' ' + str(self.order.billno),drcr=self.credit,creditamount=cgst,entity=self.order.entity,createdby= self.order.owner,entry = entryid,entrydatetime = self.order.sorderdate)
        StockTransactions.objects.filter(transactionid = self.order.id,transactiontype = self.transactiontype,account = sgstid,entity = pentity).update(accounthead = sgstid.accounthead,account= sgstid,transactiontype = self.transactiontype,transactionid = id,desc = self.description + ' ' + str(self.order.billno),drcr=self.credit,creditamount=sgst,entity=self.order.entity,createdby= self.order.owner,entry = entryid,entrydatetime = self.order.sorderdate)
        StockTransactions.objects.filter(transactionid = self.order.id,transactiontype = self.transactiontype,account = self.order.accountid,entity = pentity).update(accounthead= self.order.accountid.accounthead,account= self.order.accountid,transactiontype = self.transactiontype,transactionid = id,desc = self.description + ' ' + str(self.order.billno),drcr=self.debit,debitamount=gtotal,entity=self.order.entity,createdby= self.order.owner,entry = entryid,entrydatetime = self.order.sorderdate)
        
        return id


    def createtransactiondetails(self,detail,stocktype):

        if (detail.orderqty ==0.00):
                qty = detail.pieces
        else:
                qty = detail.orderqty
        entryid,created  = entry.objects.get_or_create(entrydate1 = self.order.sorderdate)
        details = StockTransactions.objects.create(accounthead = detail.product.saleaccount.accounthead,account= detail.product.saleaccount,stock=detail.product,transactiontype = self.transactiontype,transactionid = self.order.id,desc = self.description + ' ' + str(self.order.billno),stockttype = stocktype,salequantity = qty,drcr = self.debit,creditamount = detail.amount,cgstdr = detail.cgst,sgstdr= detail.sgst,igstdr = detail.igst,entrydate = self.order.sorderdate,entity = self.order.entity,createdby = self.order.owner,entry = entryid)
        goodstransaction.objects.create(account= detail.product.saleaccount,stock=detail.product,transactiontype = self.transactiontype,transactionid = self.order.id,stockttype = stocktype,salequantity = qty,entrydatetime = self.order.sorderdate,entity = self.order.entity,createdby = self.order.owner,entry = entryid)

        return details

    def updatetranasationdetails(self,updateddetails,stocktype):
        if (updateddetails.orderqty ==0.00):
                qty = updateddetails.pieces
        else:
                qty = updateddetails.orderqty

        details = StockTransactions.objects.filter(transactionid = self.order.id,transactiontype = self.transactiontype,account_id = updateddetails.product.saleaccount.id).create(accounthead = updateddetails.product.saleaccount.accounthead,account= updateddetails.product.saleaccount,stock=updateddetails.product,transactiontype = self.transactiontype,transactionid = self.order.id,desc = 'Purchase By V.No' + str(self.order.voucherno),stockttype = stocktype,purchasequantity = qty,drcr = self.debit,debitamount = updateddetails.amount,cgstdr = updateddetails.cgst,sgstdr= updateddetails.sgst,igstdr = updateddetails.igst,entrydate = self.order.billdate,entity = self.order.entity,createdby = self.order.createdby)
        #details = StockTransactions.objects.filter(transactionid = instance.id,transactiontype = 'P',account_id = inv_item.product.purchaseaccount.id).create(accounthead = inv_item.product.purchaseaccount.accounthead,account= inv_item.product.purchaseaccount,stock=inv_item.product,transactiontype = 'P',transactionid = inv_item.id,desc = 'Purchase By V.No',stockttype = 'P',purchasequantity = qty,drcr = 1,debitamount = inv_item.amount,cgstdr = inv_item.cgst,sgstdr= inv_item.sgst,igstdr = inv_item.igst,entrydate = instance.billdate,entity = instance.entity,createdby = instance.createdby)

        return details





class journaldetailsSerializer(serializers.ModelSerializer):
    #entityUser = entityUserSerializer(many=True)
    id = serializers.IntegerField(required=False)
    accountname = serializers.SerializerMethodField()

    class Meta:
        model = journaldetails
        fields =  ('id','account','accountname','desc','drcr','debitamount','creditamount','entity',)

    def get_accountname(self,obj):
         return obj.account.accountname



class journalmainSerializer(serializers.ModelSerializer):
    journaldetails = journaldetailsSerializer(many=True)
    class Meta:
        model = journalmain
        fields = ('id','voucherdate','voucherno','vouchertype','mainaccountid','entrydate','entity','createdby','journaldetails',)


    

    def create(self, validated_data):
        #print(validated_data)
        journaldetails_data = validated_data.pop('journaldetails')
        order = journalmain.objects.create(**validated_data)
       # stk = stocktransactionsale(order, transactiontype= 'S',debit=1,credit=0,description= 'Sale ')
        #print(tracks_data)
        for journaldetail_data in journaldetails_data:
            detail = journaldetails.objects.create(Journalmain = order, **journaldetail_data)
            id,created  = entry.objects.get_or_create(entrydate1 = order.entrydate)
            StockTransactions.objects.create(accounthead= detail.account.accounthead,account= detail.account,transactiontype = order.vouchertype,transactionid = order.id,desc = 'Journal V.No' + str(order.voucherno),drcr=detail.drcr,creditamount=detail.creditamount,debitamount=detail.debitamount,entity=order.entity,createdby= order.createdby,entrydate = order.entrydate,entry =id,entrydatetime = order.entrydate)
           # stk.createtransactiondetails(detail=detail,stocktype='S')

            # if(detail.orderqty ==0.00):
            #     qty = detail.pieces
            # else:
            #     qty = detail.orderqty
            # StockTransactions.objects.create(accounthead = detail.product.saleaccount.accounthead,account= detail.product.saleaccount,stock=detail.product,transactiontype = 'S',transactionid = order.id,desc = 'Sale By B.No ' + str(order.billno),stockttype = 'S',salequantity = qty,drcr = 0,creditamount = detail.amount,cgstcr = detail.cgst,sgstcr= detail.sgst,igstcr = detail.igst,entrydate = order.sorderdate,entity = order.entity,createdby = order.owner)

       # stk.createtransaction()
        return order

    def update(self, instance, validated_data):
        fields = ['voucherdate','voucherno','vouchertype','mainaccountid','entrydate','entity','createdby',]
        for field in fields:
            try:
                setattr(instance, field, validated_data[field])
            except KeyError:  # validated_data may not contain all fields during HTTP PATCH
                pass
        instance.save()
       # stk = stocktransactionsale(instance, transactiontype= 'S',debit=1,credit=0,description= 'Sale')
        journaldetails.objects.filter(Journalmain=instance,entity = instance.entity).delete()
        StockTransactions.objects.filter(entity = instance.entity,transactiontype = instance.vouchertype,transactionid = instance.id).delete()
     #   stk.updateransaction()

        journaldetails_data = validated_data.get('journaldetails')

        for journaldetail_data in journaldetails_data:
            detail = journaldetails.objects.create(Journalmain = instance, **journaldetail_data)
            StockTransactions.objects.create(accounthead= detail.account.accounthead,account= detail.account,transactiontype = instance.vouchertype,transactionid = instance.id,desc = 'Journal V.No' + str(instance.voucherno),drcr=detail.drcr,creditamount=detail.creditamount,debitamount=detail.debitamount,entity=instance.entity,createdby= instance.createdby,entrydate = instance.entrydate,entrydatetime = instance.entrydate)
            #stk.createtransactiondetails(detail=detail,stocktype='S')

        
        return instance


class stockdetailsSerializer(serializers.ModelSerializer):
    #entityUser = entityUserSerializer(many=True)
    id = serializers.IntegerField(required=False)
    productname = serializers.SerializerMethodField()

    class Meta:
        model = stockdetails
        fields =  ('id','stock','productname','desc','issuereceived','issuedquantity','recivedquantity','entity',)

    def get_productname(self,obj):
         return obj.stock.productname



class stockmainSerializer(serializers.ModelSerializer):
    stockdetails = stockdetailsSerializer(many=True)
    class Meta:
        model = stockmain
        fields = ('id','voucherdate','voucherno','vouchertype','entrydate','entity','createdby','stockdetails',)


    

    def create(self, validated_data):
        #print(validated_data)
        journaldetails_data = validated_data.pop('stockdetails')
        order = stockmain.objects.create(**validated_data)
       # stk = stocktransactionsale(order, transactiontype= 'S',debit=1,credit=0,description= 'Sale ')
        #print(tracks_data)
        for journaldetail_data in journaldetails_data:
            detail = stockdetails.objects.create(stockmain = order, **journaldetail_data)
            id,created  = entry.objects.get_or_create(entrydate1 = order.entrydate)
            goodstransaction.objects.create(account= detail.stock.purchaseaccount,stock=detail.stock,transactiontype = order.vouchertype,transactionid = order.id,stockttype = detail.issuereceived,issuedquantity = detail.issuedquantity,recivedquantity = detail.recivedquantity,entrydate = order.entrydate,entity = order.entity,createdby = order.createdby,entry = id)
          #  StockTransactions.objects.create(accounthead= detail.account.accounthead,account= detail.account,transactiontype = order.vouchertype,transactionid = order.id,desc = 'Journal V.No' + str(order.voucherno),drcr=detail.drcr,creditamount=detail.creditamount,debitamount=detail.debitamount,entity=order.entity,createdby= order.createdby,entrydate = order.entrydate,entry =id,entrydatetime = order.entrydate)
           # stk.createtransactiondetails(detail=detail,stocktype='S')

            # if(detail.orderqty ==0.00):
            #     qty = detail.pieces
            # else:
            #     qty = detail.orderqty
            # StockTransactions.objects.create(accounthead = detail.product.saleaccount.accounthead,account= detail.product.saleaccount,stock=detail.product,transactiontype = 'S',transactionid = order.id,desc = 'Sale By B.No ' + str(order.billno),stockttype = 'S',salequantity = qty,drcr = 0,creditamount = detail.amount,cgstcr = detail.cgst,sgstcr= detail.sgst,igstcr = detail.igst,entrydate = order.sorderdate,entity = order.entity,createdby = order.owner)

       # stk.createtransaction()
        return order

    def update(self, instance, validated_data):
        fields = ['voucherdate','voucherno','vouchertype','entrydate','entity','createdby',]
        for field in fields:
            try:
                setattr(instance, field, validated_data[field])
            except KeyError:  # validated_data may not contain all fields during HTTP PATCH
                pass
        instance.save()
       # stk = stocktransactionsale(instance, transactiontype= 'S',debit=1,credit=0,description= 'Sale')
        stockdetails.objects.filter(stockmain=instance,entity = instance.entity).delete()
        goodstransaction.objects.filter(entity = instance.entity,transactiontype = instance.vouchertype,transactionid = instance.id).delete()
     #   stk.updateransaction()

        journaldetails_data = validated_data.get('stockdetails')
        entryid,created  = entry.objects.get_or_create(entrydate1 = instance.entrydate)

        for journaldetail_data in journaldetails_data:
            detail = stockdetails.objects.create(stockmain = instance, **journaldetail_data)
            goodstransaction.objects.create(account= detail.stock.purchaseaccount,stock=detail.stock,transactiontype = instance.vouchertype,transactionid = instance.id,stockttype = detail.issuereceived,issuedquantity = detail.issuedquantity,recivedquantity = detail.recivedquantity,entrydate = instance.entrydate,entity = instance.entity,createdby = instance.createdby,entry = entryid)
            #stk.createtransactiondetails(detail=detail,stocktype='S')

        
        return instance










class salesOrderdetailsSerializer(serializers.ModelSerializer):
    #entityUser = entityUserSerializer(many=True)
    id = serializers.IntegerField(required=False)
    productname = serializers.SerializerMethodField()

    class Meta:
        model = salesOrderdetails
        fields =  ('id','product','productname','productdesc','orderqty','pieces','rate','amount','cgst','sgst','igst','linetotal','entity',)

    def get_productname(self,obj):
        return obj.product.productname


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
        salesOrderdetails.objects.filter(salesorderheader=instance,entity = instance.entity).delete()
        stk.updateransaction()

        salesOrderdetails_data = validated_data.get('salesorderdetails')

        for PurchaseOrderDetail_data in salesOrderdetails_data:
            detail = salesOrderdetails.objects.create(salesorderheader = instance, **PurchaseOrderDetail_data)
            stk.createtransactiondetails(detail=detail,stocktype='S')

        
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


class purchasereturndetailsSerializer(serializers.ModelSerializer):
    #entityUser = entityUserSerializer(many=True)
    id = serializers.IntegerField(required=False)
    productname = serializers.SerializerMethodField()

    class Meta:
        model = Purchasereturndetails
        fields =  ('id','product','productname','productdesc','orderqty','pieces','rate','amount','cgst','sgst','igst','linetotal','entity',)

    def get_productname(self,obj):
        return obj.product.productname


class PurchasereturnSerializer(serializers.ModelSerializer):
    purchasereturndetails = purchasereturndetailsSerializer(many=True)

    class Meta:
        model = PurchaseReturn
        fields = ('id','sorderdate','billno','accountid','latepaymentalert','grno','vehicle','taxtype','billcash','supply','shippedto','remarks','transport','broker','tds194q','tcs206c1ch1','tcs206c1ch2','tcs206c1ch3','tcs206C1','tcs206C2','duedate','subtotal','subtotal','cgst','sgst','igst','expenses','gtotal','entity','owner','purchasereturndetails',)


    def create(self, validated_data):
        #print(validated_data)
        salesOrderdetails_data = validated_data.pop('purchasereturndetails')
        order = PurchaseReturn.objects.create(**validated_data)
        stk = stocktransactionsale(order, transactiontype= 'PR',debit=1,credit=0,description= 'Purchase Return')
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

        Purchasereturndetails.objects.filter(purchasereturn=instance,entity = instance.entity).delete()

        salesOrderdetails_data = validated_data.get('purchasereturndetails')

        for PurchaseOrderDetail_data in salesOrderdetails_data:
            detail = Purchasereturndetails.objects.create(purchasereturn = instance, **PurchaseOrderDetail_data)
            stk.createtransactiondetails(detail=detail,stocktype='PR')

        
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




class PurchaseOrderDetailsSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    productname = serializers.SerializerMethodField()
   # productdesc1 = serializers.SerializerMethodField()
    #entityUser = entityUserSerializer(many=True)

    class Meta:
        model = PurchaseOrderDetails
        fields = ('id','product','productname','productdesc','orderqty','pieces','rate','amount','cgst','sgst','igst','linetotal','entity',)
    
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
    entrydate1 = serializers.SerializerMethodField()


    

    def get_entrydate1(self, obj):
        return obj.entry.entrydate1


    class Meta:
        model = StockTransactions
        fields = ['accounthead','account','transactiontype','debitamount','creditamount','entrydatetime','entrydate1']



class goodsserilaizer(serializers.ModelSerializer):

    # # debit  = serializers.SerializerMethodField()
    entrydate1 = serializers.SerializerMethodField()


    

    def get_entrydate1(self, obj):
        return obj.entry.entrydate1


    class Meta:
        model = goodstransaction
        fields = ['account','stock','transactiontype','purchasequantity','issuedquantity','recivedquantity','salequantity','entrydatetime','entrydate1']





class cashserializer(serializers.ModelSerializer):


    cashtrans = stocktranserilaizer(source = 'account_transactions', many=True, read_only=True)
    debit  = serializers.SerializerMethodField()
    credit = serializers.SerializerMethodField()


   # stk = stocktranserilaizer(many=True, read_only=True)
   # select_related_fields = ('accounthead')

    # debit  = serializers.SerializerMethodField()
   # day = serializers.CharField()

    class Meta:
        model = entry
        fields = ['entrydate1','debit','credit','cashtrans']

    def get_debit(self, obj):
        # fromDate = parse_datetime(self.context['request'].query_params.get(
        #     'fromDate') + ' ' + '00:00:00').strftime('%Y-%m-%d %H:%M:%S')
        # toDate = parse_datetime(self.context['request'].query_params.get(
        #     'toDate') + ' ' + '00:00:00').strftime('%Y-%m-%d %H:%M:%S')
        return obj.cashtrans.aggregate(Sum('debitamount'))['debitamount__sum']

    def get_credit(self, obj):
        # fromDate = parse_datetime(self.context['request'].query_params.get(
        #     'fromDate') + ' ' + '00:00:00').strftime('%Y-%m-%d %H:%M:%S')
        # toDate = parse_datetime(self.context['request'].query_params.get(
        #     'toDate') + ' ' + '00:00:00').strftime('%Y-%m-%d %H:%M:%S')
        return obj.cashtrans.aggregate(Sum('creditamount'))['creditamount__sum']





class stockserializer(serializers.ModelSerializer):


    goods = goodsserilaizer(source = 'account_transactions', many=True, read_only=True)
    salequantity  = serializers.SerializerMethodField()
    purchasequantity = serializers.SerializerMethodField()
    issuedquantity  = serializers.SerializerMethodField()
    recivedquantity = serializers.SerializerMethodField()


   # stk = stocktranserilaizer(many=True, read_only=True)
   # select_related_fields = ('accounthead')

    # debit  = serializers.SerializerMethodField()
   # day = serializers.CharField()

    class Meta:
        model = Product
        fields = ['productname','salequantity','purchasequantity','issuedquantity','recivedquantity','goods']

    def get_salequantity(self, obj):

        print(obj)
        # fromDate = parse_datetime(self.context['request'].query_params.get(
        #     'fromDate') + ' ' + '00:00:00').strftime('%Y-%m-%d %H:%M:%S')
        # toDate = parse_datetime(self.context['request'].query_params.get(
        #     'toDate') + ' ' + '00:00:00').strftime('%Y-%m-%d %H:%M:%S')
        return obj.goods.aggregate(Sum('salequantity'))['salequantity__sum']

    def get_purchasequantity(self, obj):
        # fromDate = parse_datetime(self.context['request'].query_params.get(
        #     'fromDate') + ' ' + '00:00:00').strftime('%Y-%m-%d %H:%M:%S')
        # toDate = parse_datetime(self.context['request'].query_params.get(
        #     'toDate') + ' ' + '00:00:00').strftime('%Y-%m-%d %H:%M:%S')
        return obj.goods.aggregate(Sum('purchasequantity'))['purchasequantity__sum']

    def get_issuedquantity(self, obj):
        return obj.goods.aggregate(Sum('issuedquantity'))['issuedquantity__sum']

    def get_recivedquantity(self, obj):
        return obj.goods.aggregate(Sum('recivedquantity'))['recivedquantity__sum']
    





   




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
    entrydate = serializers.DateTimeField(source='entrydatetime')
    desc = serializers.CharField(max_length=500)
   

    class Meta:
        model = StockTransactions
        fields = ['accountname','transactiontype','transactionid','debit','credit','entrydate','desc']


        

        # def to_representation(self, instance):
        #     original_representation = super().to_representation(instance)

        #     print(original_representation)

        #     representation = {
                
        #         'detail': original_representation,
        #     }

        #     return representation





    


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
        model = journalmain
        fields =  ['newvoucher']


class stockVSerializer(serializers.ModelSerializer):
    #entityUser = entityUserSerializer(many=True)
  #  id = serializers.IntegerField(required=False)

    newvoucher = serializers.SerializerMethodField()

    def get_newvoucher(self, obj):
        if not obj.voucherno:
            return 1
        else:
            return obj.voucherno + 1

    class Meta:
        model = stockmain
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
    productname = serializers.SerializerMethodField()
    #entityUser = entityUserSerializer(many=True)

    class Meta:
        model = salereturnDetails
        fields = ('id','product','productname','productdesc','orderqty','pieces','rate','amount','cgst','sgst','igst','linetotal','entity',)

    def get_productname(self,obj):
        return obj.product.productname




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
        stk = stocktransaction(instance, transactiontype= 'SR',debit=1,credit=0,description= 'updated')
        stk.updateransaction()
        instance.save()
        salereturnDetails.objects.filter(salereturn=instance,entity = instance.entity).delete()

        PurchaseOrderDetails_data = validated_data.get('salereturndetails')

        for PurchaseOrderDetail_data in PurchaseOrderDetails_data:
            detail = salereturnDetails.objects.create(salereturn = instance,**PurchaseOrderDetail_data)
            stk.createtransactiondetails(detail=detail,stocktype='SR')

        

        
        return instance

  








