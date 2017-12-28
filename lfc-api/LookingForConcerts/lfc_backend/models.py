from django.db import models
#from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser

from django.utils.translation import ugettext_lazy as _
from .managers import UserManager
from django.core.validators import MaxValueValidator, MinValueValidator # for integer constraints
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

import datetime


# Models in our Database.

class RegisteredUser(AbstractUser):
    """Registered User class"""
    # FIELDS COMING FROM AbstracUser

    # username
    # email
    # password
    # is_staff
    # first_name
    # last_name

    # For recommendations
    # if the user connects his account with Spotify
    spotify_id = models.CharField(_('spotify_id'), max_length=50,null=True, blank=True)
    spotify_display_name = models.CharField(_('spotify_display_name'),max_length=50,null=True, blank=True)
    spotify_refresh_token = models.CharField(_('spotify_refresh_token'),max_length=50,null=True, blank=True)

    email = models.EmailField(
        _('Email Address'), blank=False, unique=True,
        error_messages={
            'unique': _("A user with that email already exists."),
        }
    )
    birth_date = models.DateField(_('birth_date'), null=True, blank=True)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    image = models.CharField(max_length=300, null=True, blank=True)
    followers = models.ManyToManyField("self", symmetrical=False, related_name = 'following')

class Location(models.Model):
    location_id = models.AutoField(primary_key=True)
    # venue and coordinates should be retrieved from Google API.
    # charfields are placeholders for now.
    venue = models.CharField(max_length = 200)
    coordinates = models.CharField(max_length=200)

class Tag(models.Model):
    '''
    '''
    tag_id = models.AutoField(primary_key=True)
    value = models.CharField(max_length=20)
    context = models.CharField(max_length=200, blank=True)
    wikidata_uri = models.CharField(max_length=50, blank=True)

class Artist(models.Model):
    #images - implemented in Image --ONE TO MANY
    #concerts - implemented on Concert --ONE TO MANY
    name = models.CharField(max_length= 150)
    spotify_id = models.CharField(max_length= 150, unique=True)

class Image(models.Model):
    artist = models.ForeignKey(Artist, related_name = 'images', on_delete = models.CASCADE, null = True)
    height  = models.IntegerField()
    url = models.URLField()
    width = models.IntegerField()

class Concert(models.Model):
    concert_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length= 150)
    artist = models.ForeignKey(Artist, related_name = 'concerts', on_delete = models.DO_NOTHING, null = True)
    location = models.ForeignKey(Location, related_name = 'concerts', on_delete = models.CASCADE,  null=True)
    attendees = models.ManyToManyField(RegisteredUser, related_name = 'concerts')
    # tags - implemented in tag --MANY TO MANY
    tags = models.ManyToManyField(Tag, related_name = 'concerts', blank=True)
    # comments - implemented in comment - ONE TO MANY
    date_time = models.CharField(max_length=50)
    description =  models.CharField(max_length=2000, blank=True)
    price_min = models.IntegerField()
    price_max = models.IntegerField()
    seller_url = models.CharField(max_length = 300, null= True)
    image = models.CharField(max_length=300, null=True, blank=True)

    #ratings -implemented in Rating
    #concertReports -implemented in Report --ONE TO MANY

    class Meta: # artist and date_time combination should be unique for concerts!
        unique_together = ("artist", "date_time")

class Comment(models.Model):
    comment_id = models.AutoField(primary_key=True)
    owner = models.ForeignKey(RegisteredUser, related_name = 'comments', on_delete = models.CASCADE , null = True) #----------> Needs session functionality
    concert_id = models.ForeignKey(Concert, related_name = 'comments', on_delete = models.CASCADE, null = True)
    content = models.CharField(max_length = 600, default = "")

class UserReport(models.Model):
    '''
        Reports to ban users that conduct abusive behavior
    '''
    user_report_id = models.AutoField(primary_key=True)
    reporter = models.ForeignKey(RegisteredUser, related_name = 'sent_user_reports', on_delete = models.CASCADE, null=True)
    reported = models.ForeignKey(RegisteredUser, related_name = 'received_user_reports', on_delete = models.CASCADE, null=True)
    reason = models.CharField(max_length=250) # reason for reporting the user
    class Meta:
        unique_together=("reporter", "reported")

class ConcertReport(models.Model):
    '''
        Reports to correct wrong concert information
    '''
    concert_report_id = models.AutoField(primary_key=True)
    reporter = models.ForeignKey(RegisteredUser, related_name = 'concert_reports', on_delete = models.CASCADE, null=True)
    REPORT_TYPES = (
        ("NAME","name"),
        ("ARTIST","artist"),
        ("DATE_TIME","date_time"),
        ("DESCRIPTION","description"),
        ("LOCATION","location"),
        ("MIN_PRICE","min_price"),
        ("MAX_PRICE","max_price"),
        ("SELLER_URL","seller_url"),
        ("IMAGE","image"),
    )
    report_type = models.CharField(choices=REPORT_TYPES, max_length=20, blank=False)
    concert = models.ForeignKey(Concert, related_name = 'reports',on_delete = models.CASCADE, null=True)
    suggestion = models.CharField(max_length=1000)  # the suggestion as an alternative to the reported information.
    upvoters = models.ManyToManyField(RegisteredUser, related_name = 'upvoted_concert_reports', blank=True)

class Rating(models.Model):
    '''
    '''
    rating_id = models.AutoField(primary_key=True)
    owner = models.ForeignKey(RegisteredUser, related_name = 'concert_ratings', on_delete = models.CASCADE, null=True)
    concert = models.ForeignKey(Concert, related_name = 'ratings', on_delete = models.CASCADE, null=True)

    concert_atmosphere = models.IntegerField(validators=[MaxValueValidator(5), MinValueValidator(1)], null=True)
    artist_costumes = models.IntegerField(validators=[MaxValueValidator(5), MinValueValidator(1)], null=True)
    music_quality = models.IntegerField(validators=[MaxValueValidator(5), MinValueValidator(1)], null=True)
    stage_show = models.IntegerField(validators=[MaxValueValidator(5), MinValueValidator(1)], null=True)

    class Meta: # a user can rate a concert only once.
        unique_together = ("owner", "concert")

# W3C Standard Annotation model: https://www.w3.org/TR/annotation-model/
# Each Annotation is connected to a Concert object and has a RegisteredUser creator
class Annotation(models.Model):

    MOTIVATIONS = (
    ('ASSESSING', 'assessing'),
    ('BOOKMARKING', 'bookmarking'),
    ('CLASSIFYING', 'classifying'),
    ('COMMENTING', 'commenting'),
    ('DESCRIBING', 'describing'),
    ('EDITING', 'editing'),
    ('HIGHLIGHTING', 'highlighting'),
    ('IDENTIFYING', 'identifying'),
    ('LINKING', 'linking'),
    ('MODERATING', 'moderating'),
    ('QUESTIONING', 'questioning'),
    ('REPLYING', 'replying'),
    ('TAGGING', 'tagging'),
    )
    # we do not use rights field

    # id created automatically
    annotation_id = ("http://" + settings.HOST + ":" + settings.FRONTEND_PORT + "/annotations/{}").format(id)
    context = models.URLField(null=False, default="http://www.w3.org/ns/anno.jsonld")
    type = models.CharField(max_length=255, null=False, default="Annotation")
    motivation = models.CharField(choices=MOTIVATIONS, max_length=20, null=True) # the reason for creating this annotation
    creator = models.ForeignKey(RegisteredUser, related_name="annotations", on_delete=models.CASCADE, null=True)
    created = models.DateTimeField(auto_now_add=True)
    upvotes = models.IntegerField(null = True)
class AnnotationBodyAndTargetCommon(models.Model):
    TYPES = (
    ('TEXT', 'Text'),
    ('VIDEO', 'Video'),
    ('AUDIO', 'Audio'),
    ('IMAGE', 'Image'),
    )

    MIMES = (
    ('TEXT', (
            ('PLAINTEXT', 'text/plain'),
        )
    ),
    ('VIDEO', (
            ('MPEGVIDEO', 'video/mpeg'),
            ('AVIVIDEO', 'video/avi'),
        )
    ),
    ('IMAGE', (
            ('PNGIMAGE', 'image/png'),
            ('BMPIMAGE', 'image/bmp'),
            ('GIFIMAGE', 'image/gif'),
            ('JPEGIMAGE', 'image/jpeg'),
        )
    ),
    ('AUDIO', (
            ('MIDIAUDIO', 'audio/midi'),
            ('MPEGAUDIO', 'audio/mpeg'),
        )
    ),
    ('unknown', 'Unknown'),
    )

    type = models.CharField(choices=TYPES, max_length=10)
    format = models.CharField(choices=MIMES, max_length=15)

    class Meta:
        abstract = True

# the body for our Annotation class
class AnnotationBody(AnnotationBodyAndTargetCommon):
    PURPOSES = (
        ('ASSESSING', 'assessing'),
        ('BOOKMARKING', 'bookmarking'),
        ('CLASSIFYING', 'classifying'),
        ('COMMENTING', 'commenting'),
        ('DESCRIBING', 'describing'),
        ('EDITING', 'editing'),
        ('HIGHLIGHTING', 'highlighting'),
        ('IDENTIFYING', 'identifying'),
        ('LINKING', 'linking'),
        ('MODERATING', 'moderating'),
        ('QUESTIONING', 'questioning'),
        ('REPLYING', 'replying'),
        ('TAGGING', 'tagging'),
    )
    annotation = models.ForeignKey(Annotation, related_name="body", on_delete=models.CASCADE, null=True)
    purpose = models.CharField(choices=PURPOSES, max_length=20, null=True)
    value = models.CharField(max_length=255, null=False)

# the target for our Annotation class
class AnnotationTarget(AnnotationBodyAndTargetCommon):
    annotation = models.ForeignKey(Annotation, related_name="target", on_delete=models.CASCADE, null=True)
    target_id = models.CharField(max_length=255, null=False, default=("http://" + settings.HOST + ":" + settings.FRONTEND_PORT + "/concert/null"))

# W3C Specification for selectors
# 4.2 Selectors
# Many Annotations refer to part of a resource, rather than all of it, as the Target.
# We call that part of the resource a Segment (of Interest).
# A Selector is used to describe how to determine the Segment from within the Source resource.
# The nature of the Selector will be dependent on the type of resource, as the methods
# to describe Segments from various media-types will differ.
# Multiple Selectors can be given to describe the same Segment in different ways
# in order to maximize the chances that it will be discoverable later, and that
# the consuming user agent will be able to use at least one of the Selectors.

# Fragment Selector
class Selector(models.Model):
    SPECIFICATIONS = (
        ('HTML', 'http://tools.ietf.org/rfc/rfc3236'),# HTML
        ('TEXT', 'http://tools.ietf.org/rfc/rfc5147'),# Plain Text
        ('MEDIA', 'http://www.w3.org/TR/media-frags/'), # Media
        ('IMAGE', 'http://www.w3.org/TR/SVG/'),# SVG
    )
    target = models.ForeignKey(AnnotationTarget, related_name="selector", on_delete=models.CASCADE)
    type = models.CharField(default="FragmentSelector", max_length=25, null=False)
    conformsTo = models.CharField(choices=SPECIFICATIONS, max_length=50)
    value = models.CharField(max_length=255, null=False)
