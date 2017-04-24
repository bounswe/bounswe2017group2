from rest_framework import serializers
from concert.models import Concert, LANGUAGE_CHOICES, STYLE_CHOICES


class ConcertSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    
    # Artist of the concert, REQUIRED FIELD
    artist = serializers.CharField(required=True, max_length=20)
    # Location of the concert, REQUIRED FIELD
    location = serializers.CharField(required=True, max_length=30)
    # Date of the concert, REQUIRED FIELD
    date = serializers.CharField(required=True)
    # Minimum price of concert tickets, OPTIONAL FIELD
    minprice = serializers.IntegerField(default=0)
    # Maximum price of concert tickets, OPTIONAL FIELD
    maxprice = serializers.IntegerField(default=0)
    
    def create(self, validated_data):
        """
            Create and return a new `Concert` instance, given the validated data.
            """
        return Concert.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        """
            Update and return an existing `Concert` instance, given the validated data.
            """
        instance.artist = validated_data.get('artist', instance.artist)
        instance.location = validated_data.get('location', instance.location)
        instance.date = validated_data.get('date', instance.date)
        instance.minprice = validated_data.get('minprice', instance.minprice)
        instance.maxprice = validated_data.get('maxprice', instance.maxprice)
        instance.save()
        return instance
