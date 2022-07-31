from re import T
from django.db import models


from helpers.models import TrackingModel
from django.utils.translation import gettext as _
from Authentication.models import User 
from geography.models import country,state,district,city
from entity.models import entity

# Create your models here.


Debit = 'Debit'
Credit = 'Credit'

class accountHead(TrackingModel):
    BALANCE_TYPE = [
        (Credit, _('Credit')),
        (Debit, _('Debit'))
    ]

    Details_in_BS = [
        ('Yes', _('Yes')),
        ('No', _('No'))
    ]

    Group = [
        ('Balance_sheet', _('Balance Sheet')),
        ('P/l', _('Profit Loss'))
    ]

    name = models.CharField(max_length=200,verbose_name=_('Account Name'))
    code = models.IntegerField(verbose_name=_('Account Head Code'))
    detilsinbs =  models.CharField(max_length=50, choices = Details_in_BS, null=True,verbose_name=_('Details in Balance Sheet'))
    balanceType =  models.CharField(max_length=50,null=True,verbose_name=_('Balance Type'))
    drcreffect =   models.CharField(max_length=20,verbose_name=_('Debit/credit Effect'))
    description =   models.CharField(max_length=200,verbose_name=_('Description'),null=True)
    accountheadsr = models.ForeignKey("self",null=True,on_delete=models.CASCADE,verbose_name=_('Account head Sr'),blank=True)
    group =  models.CharField(max_length=50, choices = Group, null=True)
    entity = models.ForeignKey(entity,related_name='entity_accountheads',null=True,on_delete=models.CASCADE)
    owner = models.ForeignKey(to= User,  on_delete= models.CASCADE,null= True)

    class Meta:
        verbose_name = _('Account head')
        verbose_name_plural = _('Account Heads')
        


    
    def __str__(self):
        return f'{self.name} , {self.code}'



class account(TrackingModel):
    accounthead = models.ForeignKey(to = accountHead,related_name='accounthead_accounts', on_delete= models.CASCADE,null = True)
    accountcode = models.IntegerField(verbose_name=_('Account Code'),null=True,blank=True,default=1000)
    gstno       = models.CharField(max_length=50, null=True,verbose_name=_('Gst No'))
    accountname       = models.CharField(max_length=50, null=True,verbose_name=_('Account Name'))
    address1       = models.CharField(max_length=50, null=True,verbose_name=_('Address Line 1'))
    address2       = models.CharField(max_length=50, null=True,verbose_name=_('Address Line 2'))
    country       = models.ForeignKey(country,related_name='country',on_delete=models.CASCADE,null=True)
    state       = models.ForeignKey(to=state,on_delete=models.CASCADE,null=True)
    district    = models.ForeignKey(to=district,on_delete=models.CASCADE,null=True)
    city       = models.ForeignKey(to=city,on_delete=models.CASCADE,null=True)
    openingbcr = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True,verbose_name=_('Opening Balance Cr'))
    openingbdr = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True,verbose_name=_('Opening Balance Dr'))
    contactno       =models.CharField(max_length=50, null=True,verbose_name=_('Contact no'))
    pincode       =models.CharField(max_length=50, null=True,verbose_name=_('Pincode'))
    emailid       = models.CharField(max_length=50, null=True,verbose_name=_('Email id'))
    agent       = models.CharField(max_length=50, null=True,verbose_name=_('Agent/Group'))
    pan       = models.CharField(max_length=50, null=True,verbose_name=_('PAN'))
    tobel10cr       = models.BooleanField(verbose_name=_('Turnover below 10 lac'),null=True)
    approved       = models.BooleanField(verbose_name=_('Wheather aproved'),null=True)
    tdsno       = models.CharField(max_length=50, null=True,verbose_name=_('Tds A/c No'))
    entity = models.ForeignKey(entity,null=True,on_delete=models.CASCADE,)
    accountno       = models.CharField(max_length=50, null=True,verbose_name=_('Account no'))
    rtgsno          = models.CharField(max_length=50, null=True,verbose_name=_('Rtgs no'))
    bankname          = models.CharField(max_length=50, null=True,verbose_name=_('Bank Name'))
    Adhaarno          = models.CharField(max_length=50, null=True,verbose_name=_('Adhaar No'))
    saccode          = models.CharField(max_length=50, null=True,verbose_name=_('SAC Code'))
    contactperson       = models.CharField(max_length=50, null=True,verbose_name=_('Contact Person'))
    deprate             = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True,verbose_name=_('Depreciaion Rate'))
    tdsrate             = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True,verbose_name=_('TDS Rate'))
    gstshare            = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True,verbose_name=_('Adhaar No'))
    quanity1            = models.IntegerField(verbose_name=_('Quanity 1'),null=True,blank=True)
    quanity2            = models.IntegerField(verbose_name=_('Quanity 2'),null=True,blank=True)
    BanKAcno            = models.IntegerField(verbose_name=_('Bank A/c No'),null=True,blank=True)
    composition         = models.BooleanField(verbose_name=_('Bank A/c No'),null=True,blank=True)
    owner = models.ForeignKey(to= User, on_delete= models.CASCADE,null=True,)

    def __str__(self):
        return f'{self.accountname} , {self.gstno}'

    class Meta:
        verbose_name = _('Account')
        verbose_name_plural = _('Accounts')


# class account_detials1(TrackingModel):
#     account = models.OneToOneField(account,on_delete=models.CASCADE,primary_key=True)
#     accountno       = models.CharField(max_length=50, null=True,verbose_name=_('Account no'))
#     rtgsno          = models.CharField(max_length=50, null=True,verbose_name=_('Rtgs no'))
#     bankname          = models.CharField(max_length=50, null=True,verbose_name=_('Bank Name'))
#     Adhaarno          = models.CharField(max_length=50, null=True,verbose_name=_('Adhaar No'))
#     saccode          = models.CharField(max_length=50, null=True,verbose_name=_('SAC Code'))
#     owner = models.ForeignKey(to= User, on_delete= models.CASCADE,null=True,default=1,blank=True)
#     class Meta:
#         verbose_name = _('Account Detail1')
#         verbose_name_plural = _('Account Details1')

# class account_detials2(TrackingModel):
#     account = models.OneToOneField(account,on_delete=models.CASCADE,primary_key=True)
#     contactperson       = models.CharField(max_length=50, null=True,verbose_name=_('Contact Person'))
#     deprate             = models.DecimalField(max_digits=10, decimal_places=2,default=True,blank=True,verbose_name=_('Depreciaion Rate'))
#     tdsrate             = models.DecimalField(max_digits=10, decimal_places=2,default=True,blank=True,verbose_name=_('TDS Rate'))
#     gstshare            = models.DecimalField(max_digits=10, decimal_places=2,default=True,blank=True,verbose_name=_('Adhaar No'))
#     quanity1            = models.IntegerField(verbose_name=_('Quanity 1'))
#     quanity1            = models.IntegerField(verbose_name=_('Quanity 2'))
#     BanKAcno            = models.IntegerField(verbose_name=_('Bank A/c No'))
#     composition         = models.BooleanField(verbose_name=_('Bank A/c No'))
#     owner = models.ForeignKey(to= User, on_delete= models.CASCADE,null=True,default=1,blank=True)

#     class Meta:
#         verbose_name = _('Account Detail2')
#         verbose_name_plural = _('Account Details2')


    





