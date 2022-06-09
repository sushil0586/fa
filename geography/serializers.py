from rest_framework import serializers
from geography.models import country,state,district,city






class citySerializer(serializers.ModelSerializer):

    class Meta:
        model = city
        fields = '__all__'

class cityListSerializer(serializers.ModelSerializer):

    class Meta:
        model = city
        fields = ['id','cityname','citycode','distt']


class districtSerializer(serializers.ModelSerializer):

    city = citySerializer(many=True)

    class Meta:
        model = district
        fields = '__all__'

class districtListSerializer(serializers.ModelSerializer):

   # city = citySerializer(many=True)

    class Meta:
        model = district
        fields = ['id','districtname','districtcode','state']
    

class stateSerializer(serializers.ModelSerializer):

    district = districtSerializer(many=True)

    class Meta:
        model = state
        fields = ['id','statename','district']

class stateListSerializer(serializers.ModelSerializer):

    #district = districtSerializer(many=True)

    class Meta:
        model = state
        fields = ['id','statename','statecode','country']

# class countrySerializer(serializers.ModelSerializer):

#     state = stateSerializer(many=True)

#     class Meta:
#         model = country
#         fields = ['id','CountryName','state',]

class countrySerializer(serializers.ModelSerializer):

    #state = stateSerializer(many=True)

    class Meta:
        model = country
        fields = ['id','countryname']


