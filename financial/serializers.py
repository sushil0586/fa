from rest_framework import serializers
from rest_framework.fields import ChoiceField
from financial.models import accountHead,account,account_detials1,account_detials2

from geography.serializers import countrySerializer




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
    

    class Meta:
        model = accountHead
        fields = ('id','name','code','detilsinbs','balanceType','drcreffect','description','accountheadsr','group','entity','accountHeadName',)
        #   depth = 1


    def get_accountHeadName(self,obj):
       # acc =  obj.accountHeadSr.name
        if obj.accountheadsr is None:
            return 'null'   
        else :
            return obj.accountheadsr.name


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
    
    

    


class accountSerializer(serializers.ModelSerializer):

    

    class Meta:
        model = account
        fields =  ('id','accountname','address1','address2','emailid','gstno','city',)
    
    # def to_representation(self, instance):
    #     rep = super().to_representation(instance)
    #     rep['country'] = countrySerializer(instance.country).data
    #     rep['accountHead'] = accountHeadSerializer(instance.accountHead).data
    #     return rep



class accountDetails1Serializer(serializers.ModelSerializer):

    class Meta:
        model = account_detials1
        fields = '__all__'

class accountDetails2Serializer(serializers.ModelSerializer):

    class Meta:
        model = account_detials2
        fields = '__all__'