from rest_framework import serializers
from geography.models import country,state,district,city






class citySerializer(serializers.ModelSerializer):

    class Meta:
        model = city
        fields = '__all__'


class districtSerializer(serializers.ModelSerializer):

    city = citySerializer(many=True)

    class Meta:
        model = district
        fields = '__all__'

class stateSerializer(serializers.ModelSerializer):

    district = districtSerializer(many=True)

    class Meta:
        model = state
        fields = ['id','StateName','district']

class countrySerializer(serializers.ModelSerializer):

    state = stateSerializer(many=True)

    class Meta:
        model = country
        fields = ['id','CountryName','state',]


