import imp
from django.db import models
from helpers.models import TrackingModel
from Authentication.models import User
from financial.models import account
from inventory.models import Product
from entity.models import entity


# Create your models here.

class SalesOderHeader(TrackingModel):
    #RevisonNumber =models.IntegerFieldverbose_name=_('Main category'))
    Sorderdate = models.DateField(verbose_name='Sales Order date',auto_now_add=True)
    Duedate = models.DateField(verbose_name='Due date',auto_now_add=True)
    Shipdate = models.DateField(verbose_name='Ship date',auto_now_add=True)
    Staus = models.IntegerField(verbose_name='Status',default= 1)
    SalesOrderNumber = models.IntegerField(verbose_name='Sales Order Number')
    account = models.ForeignKey(to = account, on_delete= models.CASCADE,null=True,blank=True)
    subtotal =  models.DecimalField(max_digits=10, decimal_places=2,verbose_name= 'Sub Total')
    Taxamount  = models.DecimalField(max_digits=10, decimal_places=2,verbose_name= 'Tax amount')
    Freight  = models.DecimalField(max_digits=10, decimal_places=2,verbose_name= 'Freight')
    TotalAmount  = models.DecimalField(max_digits=10, decimal_places=2,verbose_name= 'Total Amount')
    entity = models.ForeignKey(entity,on_delete=models.CASCADE,verbose_name= 'entity',null= True)
    owner = models.ForeignKey(to= User, on_delete= models.CASCADE)


    def __str__(self):
        return f'{self.account} '

class salesOrderdetails(TrackingModel):
    salesOrderHeader = models.ForeignKey(to = SalesOderHeader,related_name='salesOrderdetails', on_delete= models.CASCADE,verbose_name= 'Sale Order Number')
    product = models.ForeignKey(to = Product, on_delete= models.CASCADE,verbose_name= 'Product')
    Orderqty =  models.DecimalField(max_digits=10, decimal_places=2,verbose_name= 'Order Qty')
    UnitPrice =  models.DecimalField(max_digits=10, decimal_places=2,verbose_name= 'Unit Price')
    discountPercent =  models.DecimalField(max_digits=10, decimal_places=2,verbose_name= 'Discount Percent')
    discountAmount =  models.DecimalField(max_digits=10, decimal_places=2,verbose_name= 'Discount Amount')
    LineTotal =  models.DecimalField(max_digits=10, decimal_places=2,verbose_name= 'Line Total')
    owner = models.ForeignKey(to= User, on_delete= models.CASCADE)


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


    







