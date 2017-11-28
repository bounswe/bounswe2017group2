from django.db import models
#from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser

from django.utils.translation import ugettext_lazy as _
from .managers import UserManager
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

import datetime


# Models in our Database.

class UserImage(models.Model):
    image = models.FileField(upload_to='user/')

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
    context = models.CharField(max_length=20)

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

class ConcertImage(models.Model):
    image = models.FileField(upload_to='concert/')

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


class Report(models.Model):
    '''
    '''
    report_id = models.AutoField(primary_key=True)
    reporter = models.ForeignKey(RegisteredUser, related_name = 'reported_concerts', on_delete = models.DO_NOTHING)
    content = models.CharField(max_length=200) #<---------------------------------------------------------------- NEED TO HAVE A STRUCTURE FOR REPORT


class Concert_Report(Report):
    '''
    extends from Report class.
    '''
    report_type = models.PositiveSmallIntegerField()
    # this number indicates the type of the concert report.
    # 0: date & time
    # 1: artist
    # 2: location
    # 3: venue
    concert = models.ForeignKey(Concert, related_name = 'reports',on_delete = models.CASCADE)

class Rating(models.Model):
    '''
    '''
    rating_id = models.AutoField(primary_key=True)
    owner = models.ForeignKey(RegisteredUser, related_name = 'concert_ratings', on_delete = models.CASCADE, null=True)
    concert = models.ForeignKey(Concert, related_name = 'ratings', on_delete = models.CASCADE, null=True)
    concert_atmosphere = models.IntegerField(null=True)
    artist_costumes = models.IntegerField(null=True)
    music_quality = models.IntegerField(null=True)
    stage_show = models.IntegerField(null=True)

    class Meta: # a user can rate a concert only once.
        unique_together = ("owner", "concert")
