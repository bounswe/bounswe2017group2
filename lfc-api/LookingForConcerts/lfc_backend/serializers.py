from rest_framework import serializers
from lfc_backend.models import RegisteredUser,Concert, Tag, UserReport, ConcertReport, Location, Rating, Comment, Image, Artist
from lfc_backend.models import Annotation, AnnotationBody, AnnotationTarget, Selector
import traceback
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status

class FollowedFollowingUserSerializer(serializers.ModelSerializer):
    class Meta:
        model=RegisteredUser
        fields = ('id','username','email','first_name','last_name','birth_date','image')

class UserReportSerializer(serializers.ModelSerializer):
    reporter = serializers.PrimaryKeyRelatedField(read_only=True)
    reported = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = UserReport
        fields = ("reporter",
          "reported",
          "reason")
    def update(self, instance, validated_data):
        instance.reason = validated_data.get('reason',instance.reason)
        instance.save()
        return instance

class RegisteredUserSerializer(serializers.ModelSerializer):
    sent_user_reports = UserReportSerializer(many=True, read_only=True)
    received_user_reports = UserReportSerializer(many=True, read_only=True)
    comments = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    concerts = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    followers = FollowedFollowingUserSerializer(many=True, read_only=True)
    following = FollowedFollowingUserSerializer(many=True, read_only=True)
    class Meta:
        model=RegisteredUser
        fields = ('id','username','email','password','first_name','last_name','spotify_display_name','birth_date','date_joined','is_active','image','comments','concerts','followers','following', 'sent_user_reports', 'received_user_reports')
    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password']) # hash password
        registered_user = RegisteredUser.objects.create(**validated_data)
        return registered_user

    def update(self, instance, validated_data):
        instance.spotify_id = validated_data.get('spotify_id',instance.spotify_id)
        instance.spotify_display_name = validated_data.get('spotify_display_name',instance.spotify_display_name)
        instance.spotify_refresh_token = validated_data.get('spotify_refresh_token',instance.spotify_refresh_token)
        instance.username = validated_data.get('username',instance.username)
        instance.email = validated_data.get('email',instance.email)
        #instance.password = make_password(validated_data.get('password',instance.password))
        instance.first_name = validated_data.get('first_name',instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.birth_date = validated_data.get('birth_date', instance.birth_date)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.image = validated_data.get('image', instance.image)

        instance.save()
        return instance

class CommentSerializer(serializers.ModelSerializer):
    owner = FollowedFollowingUserSerializer(read_only=True)
    class Meta:
        model = Comment
        fields = ('content','owner',)

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('value','context','wikidata_uri')

class FullTagSerializer(serializers.ModelSerializer):
    concerts = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    class Meta:
        model = Tag
        fields = ('value','context','wikidata_uri','concerts')

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ('venue','coordinates')

    def create(self, validated_data):
        comment = Comment.objects.create(**validated_data)
        return comment

class RatingSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(read_only=True)
    concert = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Rating
        fields = ('concert_atmosphere', 'artist_costumes', 'music_quality', 'stage_show', 'owner', 'concert')

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('url','height','width')

class ArtistSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True)
    concerts = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    class Meta:
        model = Artist
        fields = ('name','spotify_id','concerts','images')

class ConcertSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    location = LocationSerializer()
    artist = ArtistSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    ratings = RatingSerializer(many=True, read_only=True)
    attendees = FollowedFollowingUserSerializer(many=True, read_only=True)
    reports = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    class Meta:
        model = Concert
        fields = ('concert_id','name','artist','date_time','description','price_min','price_max','tags','location','comments','attendees','ratings', 'image', 'seller_url', 'reports')
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
            try:
                tag = Tag.objects.get(wikidata_uri=tag_data['wikidata_uri'])#searches tag data in db
            except:
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
        instance.price_max = validated_data.get('price_max', instance.price_max)
        #needs implementing for updating tags. Note 3
        #needs implementing for updating location. Also need the outcome of Google Maps API

class ConcertReportSerializer(serializers.ModelSerializer):
    reporter = RegisteredUserSerializer(read_only=True)
    concert = ConcertSerializer(read_only=True)

    class Meta:
        model = ConcertReport
        fields = ("reporter",
          "concert",
          "report_type",
          "suggestion")

class SelectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Selector
        fields = ("type",
                  "conformsTo",
                  "value")
# ADD THESE
# class AnnotationTargetSerializer(serializers.ModelSerializer):
# class AnnotationBodySerializer(serializers.ModelSerializer):
# class AnnotationSerializer(serializers.ModelSerializer):

class AnnotationBodySerializer(serializers.ModelSerializer):
    class Meta:
        model = AnnotationBody
        fields =('type',
                 'format',
                 'purpose',
                 'value'
                 )

class AnnotationTargetSerializer(serializers.ModelSerializer):
    selector = SelectorSerializer(many=True)
    class Meta:
        model = AnnotationTarget
        fields = ('type',
                  'format',
                  'target_id',
                  'selector')
    
    def create(self, validated_data):
        selector_datas = validated_data.pop("selector")
        target = AnnotationTarget.objects.create(**validated_data)
        for selector_data in selector_datas:
            Selector.objects.create(target=target, **selector_data)
        return target


class AnnotationSerializer(serializers.ModelSerializer):
    body = AnnotationBodySerializer(many=True)
    target = AnnotationTargetSerializer(many=True)
    creator = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Annotation
        fields = ('id',
                  'annotation_id',
                  'context',
                  'creator',
                  'motivation', #Search it
                  'created',
                  'body',
                  'target')
    
    def create(self, validated_data):
        #Take body and target data to create new objects in neccessary tables
        body_datas = validated_data.pop('body')
        target_datas = validated_data.pop('target')
        #create annotation
        annotation = Annotation.objects.create(**validated_data)
        #find target objects if not available create
        for target_data in target_datas:
            targetSerializer = AnnotationTargetSerializer(data = target_data)
            if targetSerializer.is_valid():
                target_object = targetSerializer.save()
            
            #add each object to annotation's target field
            annotation.target.add(target_object)
        #create body objects
        for body_data in body_datas:
            body_object = AnnotationBody.objects.create(**body_data)
            #add each body object to annotation's body field
            annotation.body.add(body_object)
        return annotation

'''
NOTES:
1-) If a tag with the given value is already available a new one should not be created, instead the previously created tag should be referenced.
2-) object.create method adds the constructed object to its designated model table.
3-) Adding tag is easy but deleting tag requires consideration. Default delete for tag model might be enough.
4-)
'''
