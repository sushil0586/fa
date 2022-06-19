import imp
from sre_parse import Verbose
from django.db import models
from helpers.models import TrackingModel
from Authentication.models import User
from financial.models import account
from inventory.models import Product
from entity.models import entity


# Create your models here.

class SalesOderHeader(TrackingModel):
    #RevisonNumber =models.IntegerFieldverbose_name=_('Main category'))
    sorderdate = models.DateField(verbose_name='Sales Order date',auto_now_add=True)
    billno = models.IntegerField(verbose_name='Bill No',default= 1)
    accountid = models.IntegerField(verbose_name='accountid',default= 1)
    latepaymentalert = models.IntegerField(verbose_name='Late Payment Alert',default= 1)
    grno = models.CharField(max_length=50, null=True,verbose_name='GR No')
    terms = models.IntegerField(verbose_name='Terms',default= 1)
    vehicle = models.CharField(max_length=50, null=True,verbose_name='Vehicle')
    taxtype = models.IntegerField(verbose_name='Tax Type',default= 1)
    billcash = models.IntegerField(verbose_name='Bill/Cash',default= 1)
    supply = models.IntegerField(verbose_name='Supply',default= 1)
    shippedto = models.CharField(max_length=500, null=True,verbose_name='Shipped To')
    remarks = models.CharField(max_length=500, null=True,verbose_name= 'Remarks')
    transport = models.CharField(max_length=500, null=True,verbose_name='TransPort')
    broker = models.CharField(max_length=500, null=True,verbose_name='Broker')
    tds194q =  models.DecimalField(max_digits=10, decimal_places=2,default=0, verbose_name= 'TDS 194 @')
    tcs206c1ch1 =  models.DecimalField(max_digits=10, decimal_places=2,default=0 ,verbose_name= 'Tcs 206C1cH1')
    tcs206c1ch2 =  models.DecimalField(max_digits=10, decimal_places=2,default=0, verbose_name= 'Tcs 206C1cH2')
    tcs206c1ch3 =  models.DecimalField(max_digits=10, decimal_places=2,default=0, verbose_name= 'Tcs 206C1cH3')
    tcs206C1 =  models.DecimalField(max_digits=10, decimal_places=2,default=0 ,verbose_name= 'Tcs 206C1')
    tcs206C2 =  models.DecimalField(max_digits=10, decimal_places=2,default=0 ,verbose_name= 'Tcs 206C2')
    duedate = models.DateField(verbose_name='Due Date',auto_now_add=True)
    subtotal =  models.DecimalField(max_digits=10, decimal_places=2,default=0,verbose_name= 'Sub Total')
    addless =  models.DecimalField(max_digits=10, decimal_places=2,default=0,verbose_name= 'Add/Less')
    cgst =  models.DecimalField(max_digits=10, decimal_places=2,default=0,verbose_name= 'C.GST')
    sgst =  models.DecimalField(max_digits=10, decimal_places=2,default=0,verbose_name= 'S.GST')
    igst =  models.DecimalField(max_digits=10, decimal_places=2,default=0,verbose_name= 'I.GST')
    expenses =  models.DecimalField(max_digits=10, decimal_places=2,default=0,verbose_name= 'EXpenses')
    gtotal =  models.DecimalField(max_digits=10, decimal_places=2,default=0,verbose_name= 'Grand Total')
    entity = models.ForeignKey(entity,on_delete=models.CASCADE,verbose_name= 'entity',null= True)
    owner = models.ForeignKey(to= User, on_delete= models.CASCADE,null=True)


    def __str__(self):
        return f'{self.accountid} '

class salesOrderdetails(TrackingModel):
    salesorderheader = models.ForeignKey(to = SalesOderHeader,related_name='salesorderdetails', on_delete= models.CASCADE,verbose_name= 'Sale Order Number')
    product = models.ForeignKey(to = Product, on_delete= models.CASCADE,verbose_name= 'Product',null = True,default = 1)
    orderqty =  models.DecimalField(max_digits=10, decimal_places=2,verbose_name= 'Order Qty')
    pieces =  models.IntegerField(verbose_name='pieces')
    rate =  models.DecimalField(max_digits=10, decimal_places=2,verbose_name= 'Rate')
    amount =  models.DecimalField(max_digits=10, decimal_places=2,verbose_name= 'Amount')
    cgst =  models.DecimalField(max_digits=10, decimal_places=2,verbose_name= 'CGST')
    sgst =  models.DecimalField(max_digits=10,null = True,default = 1, decimal_places=2,verbose_name= 'SGST')
    igst =  models.DecimalField(max_digits=10, decimal_places=2,verbose_name= 'IGST')
    linetotal =  models.DecimalField(max_digits=10, decimal_places=2,verbose_name= 'Line Total')
    entity = models.ForeignKey(entity,on_delete=models.CASCADE,verbose_name= 'entity')
    createdby = models.ForeignKey(to= User, on_delete= models.CASCADE,null=True)


    def __str__(self):
        return f'{self.product} '


class purchaseorder(TrackingModel):
    voucherdate = models.DateField(verbose_name='Vocucher Date',auto_now_add=True)
    voucherno = models.IntegerField(verbose_name='Voucher No')
    account = models.ForeignKey(to = account, on_delete= models.CASCADE,null=True,blank=True)
    billno = models.IntegerField(verbose_name='Bill No')
    billdate = models.DateField(verbose_name='Bill Date',auto_now_add=True)
    terms = models.IntegerField(verbose_name='Terms')
    taxtype = models.IntegerField(verbose_name='TaxType')
    billcash = models.IntegerField(verbose_name='Bill/Cash')
    subtotal = models.DecimalField(max_digits=10, decimal_places=2,verbose_name= 'Sub Total')
    cgst = models.DecimalField(max_digits=10, decimal_places=2,verbose_name= 'C.GST')
    sgst = models.DecimalField(max_digits=10, decimal_places=2,verbose_name= 'S.GST')
    igst = models.DecimalField(max_digits=10, decimal_places=2,verbose_name= 'I.GST')
    expenses = models.DecimalField(max_digits=10, decimal_places=2,verbose_name= 'Expenses')
    gtotal = models.DecimalField(max_digits=10, decimal_places=2,verbose_name= 'G Total')
    entity = models.ForeignKey(entity,on_delete=models.CASCADE,verbose_name= 'entity')
    createdby = models.ForeignKey(to= User, on_delete= models.CASCADE,null=True)

    def __str__(self):
        return f'{self.account} '

class PurchaseOrderDetails(models.Model):
    purchaseorder = models.ForeignKey(to = purchaseorder,related_name='purchaseorderdetails', on_delete= models.CASCADE,verbose_name= 'Purchase Order Number')
    product = models.ForeignKey(to = Product, on_delete= models.CASCADE,verbose_name= 'Product',null = True,default = 1)
    purchasedesc = models.CharField(max_length=500, null=True,verbose_name='Purchase Desc')
    orderqty =  models.DecimalField(max_digits=10, decimal_places=2,verbose_name= 'Order Qty')
    pieces =  models.IntegerField(verbose_name='pieces')
    rate =  models.DecimalField(max_digits=10, decimal_places=2,verbose_name= 'Rate')
    amount =  models.DecimalField(max_digits=10, decimal_places=2,verbose_name= 'Amount')
    cgst =  models.DecimalField(max_digits=10, decimal_places=2,verbose_name= 'CGST')
    sgst =  models.DecimalField(max_digits=10,null = True,default = 1, decimal_places=2,verbose_name= 'SGST')
    igst =  models.DecimalField(max_digits=10, decimal_places=2,verbose_name= 'IGST')
    linetotal =  models.DecimalField(max_digits=10, decimal_places=2,verbose_name= 'Line Total')
    entity = models.ForeignKey(entity,on_delete=models.CASCADE,verbose_name= 'entity')
    createdby = models.ForeignKey(to= User, on_delete= models.CASCADE,null=True)


class salereturn(TrackingModel):
    voucherdate = models.DateField(verbose_name='Vocucher Date',auto_now_add=True)
    voucherno = models.IntegerField(verbose_name='Voucher No')
    account = models.ForeignKey(to = account, on_delete= models.CASCADE,null=True,blank=True)
    billno = models.IntegerField(verbose_name='Bill No')
    billdate = models.DateField(verbose_name='Bill Date',auto_now_add=True)
    terms = models.IntegerField(verbose_name='Terms')
    taxtype = models.IntegerField(verbose_name='TaxType')
    billcash = models.IntegerField(verbose_name='Bill/Cash')
    subtotal = models.DecimalField(max_digits=10, decimal_places=2,verbose_name= 'Sub Total')
    cgst = models.DecimalField(max_digits=10, decimal_places=2,verbose_name= 'C.GST')
    sgst = models.DecimalField(max_digits=10, decimal_places=2,verbose_name= 'S.GST')
    igst = models.DecimalField(max_digits=10, decimal_places=2,verbose_name= 'I.GST')
    expenses = models.DecimalField(max_digits=10, decimal_places=2,verbose_name= 'Expenses')
    gtotal = models.DecimalField(max_digits=10, decimal_places=2,verbose_name= 'G Total')
    entity = models.ForeignKey(entity,on_delete=models.CASCADE,verbose_name= 'entity')
    createdby = models.ForeignKey(to= User, on_delete= models.CASCADE,null=True)

    def __str__(self):
        return f'{self.account} '

class salereturnDetails(models.Model):
    salereturn = models.ForeignKey(to = salereturn,related_name='salereturndetails', on_delete= models.CASCADE,verbose_name= 'Purchase Order Number')
    product = models.ForeignKey(to = Product, on_delete= models.CASCADE,verbose_name= 'Product',null = True,default = 1)
    purchasedesc = models.CharField(max_length=500, null=True,verbose_name='Purchase Desc')
    orderqty =  models.DecimalField(max_digits=10, decimal_places=2,verbose_name= 'Order Qty')
    pieces =  models.IntegerField(verbose_name='pieces')
    rate =  models.DecimalField(max_digits=10, decimal_places=2,verbose_name= 'Rate')
    amount =  models.DecimalField(max_digits=10, decimal_places=2,verbose_name= 'Amount')
    cgst =  models.DecimalField(max_digits=10, decimal_places=2,verbose_name= 'CGST')
    sgst =  models.DecimalField(max_digits=10,null = True,default = 1, decimal_places=2,verbose_name= 'SGST')
    igst =  models.DecimalField(max_digits=10, decimal_places=2,verbose_name= 'IGST')
    linetotal =  models.DecimalField(max_digits=10, decimal_places=2,verbose_name= 'Line Total')
    entity = models.ForeignKey(entity,on_delete=models.CASCADE,verbose_name= 'entity')
    createdby = models.ForeignKey(to= User, on_delete= models.CASCADE,null=True)



class journal(TrackingModel):
    account = models.ForeignKey(to = account, on_delete= models.CASCADE,null=True,blank=True,verbose_name='Account Name')
    drcr = models.BooleanField(verbose_name='Debit/Credit')
    amount =  models.DecimalField(max_digits=10, decimal_places=2,verbose_name= 'Amount')
    entrydate = models.DateField(verbose_name='Entry Date')
    entity = models.ForeignKey(entity,on_delete=models.CASCADE,verbose_name= 'entity')
    createdby = models.ForeignKey(to= User, on_delete= models.CASCADE,null=True)




    







