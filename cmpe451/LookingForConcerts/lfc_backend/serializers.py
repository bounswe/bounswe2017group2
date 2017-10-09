from rest_framework import serializers
from lfc_backend.models import Concert, Tag, Report, Location, Rating

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('value');

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ('venue','coordinates');

class ConcertSerializer(serializers.ModelSerializer):
    #tags = TagSerializer(many=True)
    #location = LocationSerializer()

    class Meta:
        model = Concert
        #fields = ('name','artist','date_time','description','price_min','price_max','tags','location')
        fields = ('name','artist','date_time','description','price_min','price_max')

    def create(self, validated_data):
        #tags_data = validated_data.pop('tags')
        #location_data = validated_data.pop('location')
        concert = Concert.objects.create(**validated_data)
        #location.objects.create(concert = concert, **location_data)
        #for tag_data in tags_data:
        #    tag = Tag.objects.create(**tag_data)#creates tag object without the field concerts <------- NEEDS A CHANGE look at notes 1
        #    tag.concerts.add(concert) #adds concert to tags concerts field also adds tag to concerts tags field
                #<--- Stayed here
        return concert

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name',instance.name)
        instance.artist = validated_data.get('artist',instance.artist)
        instance.date_time = validated_data.get('date_time',instance.date_time)
        instance.description = validated_data.get('description',instance.date_time)
        instance.price_min = validated_data.get('price_min', instance.price_min)
        instance.price_max = validated_data.get('prica_max', instance.price_max)
        #needs implementing for updating tags. Note 3
        #needs implementing for updating location. Also need the outcome of Google Maps API
'''
CREATION PART OF CONCERT MUST HAVE BEEN DONE. CHECK FOR BUGS NEVERTHELESS.

NOTES:
1-) If a tag with the given value is already available It should't create a new one, instead it should take the tag and relate it to the concert.
2-) object.create method adds the constructed object to its designated model table.
3-) Adding tag is easy but needs thinking for delete tag. Default delete for tag model might be enough. Should think about it.
4-)
'''
