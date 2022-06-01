from rest_framework import serializers
from rest_framework.fields import ChoiceField
from financial.models import accountHead,account,account_detials1,account_detials2

from geography.serializers import countrySerializer

class accountHeadSerializer(serializers.ModelSerializer):

    detilsinbs = ChoiceField(choices=accountHead.Details_in_BS)
    #balanceType = ChoiceField(choices=accountHead.BALANCE_TYPE)
    

    class Meta:
        model = accountHead
        fields = ('id','name','code','detilsinbs','balanceType','DrcrEffect','description','accountHeadSr','group','entity',)

        # def to_representation(self, instance):
        #     rep = super(accountHeadSerializer.self).to_representation(instance)
        #     #rep['accountHeadSr'] = accountHeadSerializer(instance.accountHead).data
        #     return rep
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
        fields = '__all__'
    
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['country'] = countrySerializer(instance.country).data
        rep['accountHead'] = accountHeadSerializer(instance.accountHead).data
        return rep



class accountDetails1Serializer(serializers.ModelSerializer):

    class Meta:
        model = account_detials1
        fields = '__all__'

class accountDetails2Serializer(serializers.ModelSerializer):

    class Meta:
        model = account_detials2
        fields = '__all__'