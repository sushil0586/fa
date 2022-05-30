import imp
from django.db import models
from rest_framework import serializers
from Authentication.models import User
#from entity.models import enti
#from entity.serializers import entityUserSerializer

class Registerserializers(serializers.ModelSerializer):

    password = serializers.CharField(max_length = 128, min_length = 6, write_only = True)
    id = serializers.IntegerField(required = False)

   


    class Meta:
        model = User
        fields = ('id','username','email','password','groups',)
        extra_kwargs = {'id': {'read_only': False},
         'username': {'validators': []},
         'email': {'validators': []}}

    def create(self, validated_data):
        groups_data = validated_data.pop('groups')
        user = User.objects.create_user(**validated_data)
        for group_data in groups_data:
             # Group.objects.create(user=user, **group_data)
             user.groups.add(group_data)
        return user

class Registerserializer(serializers.ModelSerializer):

    password = serializers.CharField(max_length = 128, min_length = 6, write_only = True)

   


    class Meta:
        model = User
        fields = ('username','email','password',)

    # def create(self, validated_data):
    #     groups_data = validated_data.pop('groups')
    #     user = User.objects.create_user(**validated_data)
    #     for group_data in groups_data:
    #          # Group.objects.create(user=user, **group_data)
    #          user.groups.add(group_data)
    #     return user

class Userserializer(serializers.ModelSerializer):

    password = serializers.CharField(max_length = 128, min_length = 6, write_only = True)

   # userentity = entityUserSerializer(many=True)

    #userentity = entityUserSerializer(many=True)


    class Meta:
        model = User
        fields = ('username','email','password','groups','uentity',)
        depth = 1

    
       

class LoginSerializer(serializers.ModelSerializer):

    password = serializers.CharField(max_length = 128, min_length = 6, write_only = True)


    class Meta:
        model = User
        fields = ('email','password','token',)

        read_only_fields = ['token']





