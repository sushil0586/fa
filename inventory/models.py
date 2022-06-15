
from django.db import models
from django.db.models.deletion import CASCADE
from helpers.models import TrackingModel
from Authentication.models import User
from django.utils.translation import gettext as _
from entity.models import entity


class ProductCategory(TrackingModel):
    pcategoryname = models.CharField(max_length= 255,verbose_name=_('Product Category'))
    maincategory = models.ForeignKey("self",null=True,on_delete=models.CASCADE,verbose_name=_('Main category'),default=True,blank=True)
    entity = models.ForeignKey(entity,null=True,on_delete=models.CASCADE)
    createdby = models.ForeignKey(to= User, on_delete= models.CASCADE)


    def __str__(self):
        return f'{self.pcategoryname} '

class Product(TrackingModel):
    productname = models.CharField(max_length= 255,verbose_name=_('Product Name'))
    productcode = models.IntegerField(default=1001,blank=True,verbose_name=_('Product Code'))
    productdesc = models.CharField(max_length= 255,verbose_name=_('product desc'))
    openingstockqty = models.DecimalField(max_digits=10, decimal_places=2)
    openingstockboxqty = models.IntegerField(default=True,blank=True,verbose_name=_('Box/Pcs'))
    openingstockvalue = models.DecimalField(max_digits=10, decimal_places=2)
    productcategory = models.ForeignKey(to= ProductCategory,default=True,blank=True, on_delete= models.CASCADE,verbose_name=_('Product Category'))
    purchaserate = models.DecimalField(max_digits=10, decimal_places=2,default=True,blank=True,verbose_name=_('Purchase Rate'))
    prlesspercentage = models.DecimalField(max_digits=10, decimal_places=2)
    mrp = models.DecimalField(max_digits=10, decimal_places=2)
    mrpless = models.DecimalField(max_digits=10, decimal_places=2)
    salesprice = models.DecimalField(max_digits=10, decimal_places=2)
    totalgst = models.DecimalField(max_digits=10, decimal_places=2)
    cgst = models.DecimalField(max_digits=10, decimal_places=2)
    cgstcess = models.DecimalField(max_digits=10, decimal_places=2)
    sgst = models.DecimalField(max_digits=10, decimal_places=2)
    sgstcess = models.DecimalField(max_digits=10, decimal_places=2)
    igst = models.DecimalField(max_digits=10, decimal_places=2)
    igstcess = models.DecimalField(max_digits=10, decimal_places=2)
    is_pieces = models.BooleanField(default=True)
    is_stockable = models.BooleanField(default=True)
    entity = models.ForeignKey(entity,on_delete=models.CASCADE)
    createdby = models.ForeignKey(to= User,null=True, on_delete= models.CASCADE)

    def __str__(self):
        return f'{self.productname} '

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
            




