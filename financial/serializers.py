from sys import implementation
from rest_framework import serializers
from rest_framework.fields import ChoiceField
from financial.models import accountHead,account

from geography.serializers import countrySerializer
import os


class accountSerializer(serializers.ModelSerializer):

    

    class Meta:
        model = account
        fields =  '__all__'



class accountSerializer2(serializers.ModelSerializer):

    

    class Meta:
        model = account
        fields =  ('id','accountname','accountcode',)
    



class accountHeadMainSerializer(serializers.ModelSerializer):

    #detilsinbs = ChoiceField(choices=accountHead.Details_in_BS)
    
    #accountHeadName = serializers.SerializerMethodField()
  
    #balanceType = ChoiceField(choices=accountHead.BALANCE_TYPE)

   
    

    class Meta:
        model = accountHead
        fields = ('id','name',)
        #depth = 1






class accountHeadSerializer(serializers.ModelSerializer):

    detilsinbs = ChoiceField(choices=accountHead.Details_in_BS)
   # accountHeadMain = accountHeadMainSerializer(many=True)
    accountHeadName = serializers.SerializerMethodField()
  
    #balanceType = ChoiceField(choices=accountHead.BALANCE_TYPE)

    accounthead_accounts = accountSerializer(many= True)
    

    class Meta:
        model = accountHead
        fields = ('id','name','code','detilsinbs','balanceType','drcreffect','description','accountheadsr','group','entity','accountHeadName','accounthead_accounts',)
        #depth = 1


    def get_accountHeadName(self,obj):
       # acc =  obj.accountHeadSr.name
        if obj.accountheadsr is None:
            return 'null'   
        else :
            return obj.accountheadsr.name

    def create(self, validated_data):
        print(validated_data)
        entity1 = validated_data.get('entity')
        #user = validated_data.get('user')

        PrchaseOrderDetails_data = validated_data.pop('accounthead_accounts')
        order = accountHead.objects.create(**validated_data)
       # print(tracks_data)
        for PurchaseOrderDetail_data in PrchaseOrderDetails_data:
             account.objects.create(accounthead = order,entity=entity1, **PurchaseOrderDetail_data)
            
        return order


        print(validated_data)
        return 1
        # PurchaseOrderDetails_data = validated_data.pop('purchaseorderdetails')
        # order = purchaseorder.objects.create(**validated_data)
        # #print(tracks_data)
        # for PurchaseOrderDetail_data in PurchaseOrderDetails_data:
        #     PurchaseOrderDetails.objects.create(purchaseorder = order, **PurchaseOrderDetail_data)
        # return order


    # def to_representation(self, instance):
    #     rep = super().to_representation(instance)
    #     #rep['country'] = countrySerializer(instance.country).data
    #     rep['accountHeadName'] = accountHeadMainSerializer(instance.accountHeadSr).data
    #     return rep


    # def to_representation(self, instance):
    #     rep = super(accountHeadSerializer.self).to_representation(instance)
    #    # rep['country'] = countrySerializer(instance.country).data
    #     rep['accountHeadSr'] = accountHeadSerializer(instance.accountHeadSr).data
    #     return rep

    

        # def to_representation(self, instance):
        #     rep = super(accountHeadSerializer.self).to_representation(instance)
        #     rep.update(instance)
        #     return rep
        # def to_representation(self, value):
        #     serializer = self.parent.parent.__class__(value, context=self.context)
        #     return serializer.data

        # def get_related_field(self, model_field):
            # Handles initializing the `subcategories` field
            #return accountHeadSerializer()
        # def get_related_field(self, id):
        #     # Handles initializing the `subcategories` field
        #     return accountHeadSerializer()

        # def get_fields(self):
        #     fields = super(accountHeadSerializer, self).get_fields()
        #     fields['accountHeadSr'] = accountHeadSerializer(many=True)
        #     return fields
    
    

    



    # def to_representation(self, instance):
    #     rep = super().to_representation(instance)
    #     rep['country'] = countrySerializer(instance.country).data
    #     rep['accountHead'] = accountHeadSerializer(instance.accountHead).data
    #     return rep



