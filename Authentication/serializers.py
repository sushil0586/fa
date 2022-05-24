import imp
from django.db import models
from rest_framework import serializers
from Authentication.models import User
from entity.models import entity_user
from entity.serializers import entityUserSerializer

class Registerserializer(serializers.ModelSerializer):

    password = serializers.CharField(max_length = 128, min_length = 6, write_only = True)

    userentity = entityUserSerializer(many=True)


    class Meta:
        model = User
        fields = ('username','email','password','groups','userentity',)

    def create(self, validated_data):
        groups_data = validated_data.pop('groups')
        user = User.objects.create_user(**validated_data)
        for group_data in groups_data:
             # Group.objects.create(user=user, **group_data)
             user.groups.add(group_data)
        return user
       

class LoginSerializer(serializers.ModelSerializer):

    password = serializers.CharField(max_length = 128, min_length = 6, write_only = True)


    class Meta:
        model = User
        fields = ('email','password','token',)

        read_only_fields = ['token']




class userserializer(serializers.ModelSerializer):


    password = serializers.CharField(max_length = 128, min_length = 6, write_only = True)

    
    class Meta:
        model = User
        fields = ('username','email','first_name','last_name','password',)

