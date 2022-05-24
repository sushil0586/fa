from django.db import models
from helpers.models import TrackingModel
from django.utils.translation import gettext as _



# Create your models here.



class country(TrackingModel):
    CountryName =    models.CharField(max_length= 255)
    CountryCode =    models.CharField(max_length= 25)

    class Meta:
        verbose_name = _('Country')
        verbose_name_plural = _('Countries')


    
    def __str__(self):
        return f'{self.CountryCode} , {self.CountryName}'







class state(TrackingModel):
    StateName =    models.CharField(max_length= 255)
    StateCode =    models.CharField(max_length= 25)
    Country = models.ForeignKey(country, related_name='state', on_delete=models.CASCADE)

    
    class Meta:
        verbose_name = _('State')
        verbose_name_plural = _('States')


    
    def __str__(self):
        return f'{self.StateCode} , {self.StateName}'




class district(TrackingModel):
    districtName =    models.CharField(max_length= 255)
    districtCode =    models.CharField(max_length= 25)
    state = models.ForeignKey(state, related_name='district', on_delete=models.CASCADE)

    
    def __str__(self):
        return f'{self.districtCode} , {self.districtName}'




class city(TrackingModel):
    cityName =    models.CharField(max_length= 255)
    cityCode =    models.CharField(max_length= 25)
    distt = models.ForeignKey(district, related_name='city', on_delete=models.CASCADE)


    
    class Meta:
        verbose_name = _('City')
        verbose_name_plural = _('Cities')


    def __str__(self):
        return f'{self.cityCode} , {self.cityName}'
