from rest_framework import serializers
from concert.models import Concert,User, LANGUAGE_CHOICES, STYLE_CHOICES

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


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    
    # Name of the User, REQUIRED FIELD
    name = serializers.CharField(required=True, max_length=20)
    # Email of the User, REQUIRED FIELD
    email = serializers.CharField(required=True, max_length=30)
    # Password of the User, REQUIRED FIELD
    password = serializers.CharField(required=True)
    # Age price of User tickets, OPTIONAL FIELD
    age = serializers.IntegerField(default=0)
    
    def create(self, validated_data):
        """
            Create and return a new `User` instance, given the validated data.
            """
        return User.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        """
            Update and return an existing `User` instance, given the validated data.
            """
        instance.name = validated_data.get('name', instance.name)
        instance.email = validated_data.get('email', instance.email)
        instance.password = validated_data.get('password', instance.password)
        instance.age = validated_data.get('age', instance.age)
        instance.save()
        return instance
