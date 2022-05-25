from rest_framework import serializers
from entity.models import entity,entity_details,unitType,entity_user
#from Authentication.serializers import userserializer


class unitTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = unitType
        fields = '__all__'

class entityUserSerializer(serializers.ModelSerializer):


   # users = userserializer(many=True)

    class Meta:
        model = entity_user
        fields =  ['id','entity','user']

    # def to_representation(self, instance):
    #     rep = super().to_representation(instance)
    #     rep['user'] = (instance.user).data
       
    #     return rep


class entitySerializer(serializers.ModelSerializer):


    #entityUser = entityUserSerializer(many=True)

    

    class Meta:
        model = entity
        fields = '__all__'


class entitySerializer_load(serializers.ModelSerializer):


    entityUser = entityUserSerializer(many=True)

    

    class Meta:
        model = entity
        fields = '__all__'



class entityDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = entity_details
        fields = ('entity','style','commodity','weightDecimal','email','registrationno','division','collectorate',)