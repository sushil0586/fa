
from django.db import models
from django.db.models.deletion import CASCADE
from helpers.models import TrackingModel
from Authentication.models import User
from django.utils.translation import gettext as _
from financial.models import accountHead


class ProductCategory(TrackingModel):
    PCategoryName = models.CharField(max_length= 255,verbose_name=_('Product Category'))
    MainCategory = models.ForeignKey("self",null=True,on_delete=models.CASCADE,verbose_name=_('Main category'),default=True,blank=True)
    owner = models.ForeignKey(to= User, on_delete= models.CASCADE)


    def __str__(self):
        return f'{self.PCategoryName} '

class Product(TrackingModel):
    ProductName = models.CharField(max_length= 255,verbose_name=_('Product Name'))
    ProductDesc = models.TextField(verbose_name=_('Product Desc'))
    OpeningStockqty = models.DecimalField(max_digits=10, decimal_places=2,default=True,blank=True,verbose_name=_('Opening Stock Qty'))
    openingStockBoxqty = models.IntegerField(default=True,blank=True,verbose_name=_('Box/Pcs'))
    OpeningStockvalue = models.DecimalField(max_digits=10, decimal_places=2,default=True,blank=True,verbose_name=_('Opening Stock Value'))
    ProductCategory = models.ForeignKey(to= ProductCategory,default=True,blank=True, on_delete= models.CASCADE,verbose_name=_('Product Category'))
    Purchaserate = models.DecimalField(max_digits=10, decimal_places=2,default=True,blank=True,verbose_name=_('Purchase Rate'))
    PRlessPercentage = models.DecimalField(max_digits=10, decimal_places=2,default=True,blank=True,verbose_name=_('Less %'))
    Mrp = models.DecimalField(max_digits=10, decimal_places=2,default=True,blank=True,verbose_name=_('M.R.P'))
    MrpLess = models.DecimalField(max_digits=10, decimal_places=2,default=True,blank=True,verbose_name=_('Less %'))
    SalePrice = models.DecimalField(max_digits=10, decimal_places=2,default=True,blank=True,verbose_name=_('Sale Price'))
    Totalgst = models.DecimalField(max_digits=10, decimal_places=2,default=True,blank=True,verbose_name=_('Less %'))
    cgst = models.DecimalField(max_digits=10, decimal_places=2,default=True,blank=True,verbose_name=_('C GST @'))
    cgstcess = models.DecimalField(max_digits=10, decimal_places=2,default=True,blank=True,verbose_name=_('Cess Qty'))
    sgst = models.DecimalField(max_digits=10, decimal_places=2,default=True,blank=True,verbose_name=_('S GST @'))
    sgstcess = models.DecimalField(max_digits=10, decimal_places=2,default=True,blank=True,verbose_name=_('Cess Qty'))
    is_stockable = models.BooleanField(default=True)
    owner = models.ForeignKey(to= User, on_delete= models.CASCADE)

    def __str__(self):
        return f'{self.ProductName} '

class Album(models.Model):
    album_name = models.CharField(max_length=100)
    artist = models.CharField(max_length=100)
    owner = models.ForeignKey(to= User, on_delete= models.CASCADE)

class Track(models.Model):
    album = models.ForeignKey(Album, related_name='tracks', on_delete=models.CASCADE)
    order = models.IntegerField()
    title = models.CharField(max_length=100)
    duration = models.IntegerField()
   

    class Meta:
       ordering = ['order']

    def __str__(self):
        return '%d: %s' % (self.order, self.title)
            




