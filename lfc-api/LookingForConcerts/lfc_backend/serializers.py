from rest_framework import serializers
from lfc_backend.models import RegisteredUser,Concert, Tag, Report, Location, Rating, Comment
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ObjectDoesNotExist


class RegisteredUserSerializer(serializers.ModelSerializer):
    class Meta:
        model=RegisteredUser
        fields = ('email','password','first_name','last_name','age','date_joined','is_active','avatar','comments')
    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password']) # hash password
        registered_user = RegisteredUser.objects.create(**validated_data)
        return registered_user

class CommentSerializer(serializers.ModelSerializer):
    owner = RegisteredUserSerializer(read_only=True)
    class Meta:
        model = Comment
        fields = ('content','owner',)

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('label',)

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ('venue','coordinates')

    def create(self, validated_data):
        comment = Comment.objects.create(**validated_data)
        return comment

class ConcertSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    location = LocationSerializer()
    comments = CommentSerializer(many=True, read_only=True)
    class Meta:
        model = Concert
        fields = ('concert_id','name','artist','date_time','description','price_min','price_max','tags','location','comments')
        # location should be retrieved from Google API
        # tags should be retrieved from a 3rd party semantic tag repository such as; Wikidata.

    def create(self, validated_data):
        tags_data = validated_data.pop('tags')
        location_data = validated_data.pop('location')
        #validated_data.pop('comments');
        try:
            location = Location.objects.get(**location_data)
        except ObjectDoesNotExist:
            location = Location.objects.create(**location_data)
        concert = Concert.objects.create(**validated_data)
        for tag_data in tags_data:
            tag = Tag.objects.create(**tag_data)#creates tag object without adding concert to the concerts field<------- NEEDS A CHANGE look at notes 1
            tag.concerts.add(concert) #adds concert to tags concerts field also adds tag to concerts tags field
        location.concerts.add(concert)
        return concert

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name',instance.name)
        instance.artist = validated_data.get('artist',instance.artist)
        instance.date_time = validated_data.get('date_time',instance.date_time)
        instance.description = validated_data.get('description',instance.description)
        instance.price_min = validated_data.get('price_min', instance.price_min)
        instance.price_max = validated_data.get('prica_max', instance.price_max)
        #needs implementing for updating tags. Note 3
        #needs implementing for updating location. Also need the outcome of Google Maps API

'''
NOTES:
1-) If a tag with the given value is already available a new one should not be created, instead the previously created tag should be referenced.
2-) object.create method adds the constructed object to its designated model table.
3-) Adding tag is easy but deleting tag requires consideration. Default delete for tag model might be enough.
4-)
'''
