from rest_framework import serializers
from entity.models import entity,entity_details,unitType
from Authentication.models import User
from Authentication.serializers import Registerserializers

#from Authentication.serializers import userserializer


class unitTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = unitType
        fields = '__all__'


class entityAddSerializer(serializers.ModelSerializer):

    class Meta:
        model = entity
        fields = '__all__'


# class entityUserSerializer(serializers.ModelSerializer):


#     user_details = Registerserializers(many=False)

#     class Meta:
#         model = entity_user
#         fields =  ('id','entity','user')
#         depth = 0



# class entityUserAddSerializer(serializers.ModelSerializer):


#     user = Registerserializers(many=False)

#     class Meta:
#         model = entity_user
#         fields = '__all__'
#         #depth = 0

#     def create(self,validated_data):
#         print(validated_data)
#         user_data = self.validated_data.pop('user')

#         print(user_data)
#         user = User.objects.create_user(**user_data)
#         entity_item = entity.objects.get(id=1)
#         entity_user.objects.create(user = user, entity= entity_item)
#         #entity_user.objects.create(user = user,**validated_data)

#         return user

    # def to_representation(self, instance):
    #     rep = super().to_representation(instance)
    #     rep['user'] = (instance.user).data
       
    #     return rep


class entitySerializer(serializers.ModelSerializer):


    user = Registerserializers(many=True)

    

    class Meta:
        model = entity
        fields = ['id','unitType','entityName','address','ownerName','user',]

  

    def get_or_create_packages(self, packages):
        package_ids = []
        for package in packages:
            package_instance, created = User.objects.get_or_create(pk=package.get('id'), defaults=package)
            package_ids.append(package_instance.pk)
        return package_ids

    def create_or_update_packages(self, packages):
        package_ids = []
        for package in packages:
            package_id = package.get('id', None)
            print(package_id)

            package_instance, created = User.objects.update_or_create(pk=package.get('id'), defaults=package)
            package_ids.append(package_instance.pk)
        return package_ids

    def create(self, validated_data):
        package = validated_data.pop('user', [])
        order = entity.objects.create(**validated_data)
        order.user.set(self.get_or_create_packages(package))
        return order

    def update(self, instance, validated_data):
        package = validated_data.pop('user', [])
        instance.user.set(self.create_or_update_packages(package))
        fields = ['id','unitType','entityName','address','ownerName']
        for field in fields:
            try:
                setattr(instance, field, validated_data[field])
            except KeyError:  # validated_data may not contain all fields during HTTP PATCH
                pass
        print(list[instance])
        instance.save()
        return instance


# class entitySerializer_load(serializers.ModelSerializer):


#     entityUser = entityUserSerializer(many=True)

    

#     class Meta:
#         model = entity
#         fields = '__all__'
        

   



class entityDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = entity_details
        fields = ('entity','style','commodity','weightDecimal','email','registrationno','division','collectorate',)


   
        
        # #print(tracks_data)
        # for PurchaseOrderDetail_data in PurchaseOrderDetails_data:
        #     PurchaseOrderDetails.objects.create(purchaseOrder = order, **PurchaseOrderDetail_data)
        # return order