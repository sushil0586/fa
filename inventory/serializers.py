from rest_framework import serializers
from inventory.models import Product,Album,Track,ProductCategory,Ratecalculate,UnitofMeasurement,stkcalculateby,typeofgoods,stkvaluationby,gsttype


class ProductCategorySerializer(serializers.ModelSerializer):

    maincategoryname = serializers.SerializerMethodField()

    class Meta:
        model = ProductCategory
        fields = ('id','pcategoryname','maincategory','entity','maincategoryname',)

    def get_maincategoryname(self,obj):
       # acc =  obj.accountHeadSr.name
        if obj.maincategory is None:
            return 'null'   
        else :
            return obj.maincategory.pcategoryname

class ProductSerializer(serializers.ModelSerializer):


   # pcategoryname = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields ='__all__'

    # def get_pcategoryname(self,obj):
    #    # acc =  obj.accountHeadSr.name
    #     if obj.productcategory is None:
    #         return 'null'   
    #     else :
    #         return obj.productcategory.pcategoryname


class Trackserializer(serializers.ModelSerializer):
    #id = serializers.IntegerField()
    class Meta:
        model = Track
        fields = ('id','order','title','duration',)

class Ratecalculateserializer(serializers.ModelSerializer):
    #id = serializers.IntegerField()
    class Meta:
        model = Ratecalculate
        fields = ('id','rname','rcode',)

class UOMserializer(serializers.ModelSerializer):
    #id = serializers.IntegerField()
    class Meta:
        model = UnitofMeasurement
        fields = ('id','unitname','unitcode',)

class TOGserializer(serializers.ModelSerializer):
    #id = serializers.IntegerField()
    class Meta:
        model = typeofgoods
        fields = ('id','goodstype','goodscode',)

class GSTserializer(serializers.ModelSerializer):
    #id = serializers.IntegerField()
    class Meta:
        model = gsttype
        fields = ('id','gsttypename','gsttypecode',)


        
        

class AlbumSerializer(serializers.ModelSerializer):
    tracks = Trackserializer(many=True)

    class Meta:
        model = Album
        fields = ['id','album_name', 'artist', 'tracks',]


    def create(self, validated_data):
        print(validated_data)
        tracks_data = validated_data.pop('tracks')
        album = Album.objects.create(**validated_data)
        print(tracks_data)
        for track_data in tracks_data:
            Track.objects.create(album = album, **track_data)
        return album

    def update(self, instance, validated_data):
        instance.album_name = validated_data.get('album_name', instance.album_name)
        instance.artist = validated_data.get('artist', instance.artist)
        instance.save()

        tracks = validated_data.get('tracks')

        print(tracks)

        product_items_dict = dict((i.id, i) for i in instance.tracks.all())

       # print(product_items_dict)
        

        for track in tracks:
            track_id = track.get('id', None)
            print(track_id)
            if track_id:
                track_item = Track.objects.get(id=track_id)
                track_item.order = track.get('order', track_item.order)
                track_item.title = track.get('title', track_item.title)
                track_item.duration = track.get('duration', track_item.duration)
                track_item.save()
            else:
                Track.objects.create(album = instance, **track)

        # if len(product_items_dict) > 0:
        #     for item not in product_items_dict.values():
        #         item.delete()

        return instance

   



