from django.db import models
#from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from .managers import UserManager
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings

import datetime

# This code is triggered whenever a new user has been created and saved to the database

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

# Models in our Database.

class RegisteredUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), max_length=255,
                              unique=True, db_index=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    birth_date = models.DateTimeField(_('birth_date'), null=True, blank=True)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    is_active = models.BooleanField(_('active'), default=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    #location = models.CharField(max_length=40)
    #concerts = models.ManyToManyField(Concert, related_name= 'users')

    objects = UserManager()

    USERNAME_FIELD = 'email' # we use email as the username
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('registered_user')
        verbose_name_plural = _('registered_users')

    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        '''
        Sends an email to this User.
        '''
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def __unicode__(self):
        return '%s %s' % (self.first_name, self.last_name)


class Location(models.Model):
    location_id = models.AutoField(primary_key=True)
    # venue and coordinates should be retrieved from Google API.
    # charfields are placeholders for now.
    venue = models.CharField(max_length = 200)
    coordinates = models.CharField(max_length=200)


class Concert(models.Model):
    concert_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length= 150)
    artist = models.CharField(max_length= 50)
    location = models.ForeignKey(Location, related_name = 'concerts', on_delete = models.CASCADE,  null=True)
    users = models.ManyToManyField(RegisteredUser, related_name = 'concerts')
    # tags - implemented in tag --MANY TO MANY
    # comments - implemented in comment - ONE TO MANY
    # date_time = models.DateTimeField()
    date_time = models.CharField(max_length=50)
    description =  models.CharField(max_length=2000, blank=True)
    price_min = models.IntegerField()
    price_max = models.IntegerField()
    #attendees -will be implemented in RegisteredUser --MANY TO MANY
    #ratings -implemented in Rating
    #concertReports -implemented in Report --ONE TO MANY

    class Meta: # artist and date_time combination should be unique for concerts!
        unique_together = ("artist", "date_time")

class Comment(models.Model):
    comment_id = models.AutoField(primary_key=True)
    owner = models.ForeignKey(RegisteredUser, related_name = 'comments', on_delete = models.CASCADE , null = True) #----------> Needs session functionality
    concert_id = models.ForeignKey(Concert, related_name = 'comments', on_delete = models.CASCADE, null = True)
    content = models.CharField(max_length = 600, default = "")


class Tag(models.Model):
    '''
    '''
    tag_id = models.AutoField(primary_key=True)
    concerts = models.ManyToManyField(Concert, related_name = 'tags') #might need on_delete = DO_NOTHING but couldn't find on_delete as a parameter in its documentation
    label = models.CharField(max_length=50)


class Report(models.Model):
    '''
    '''
    report_id = models.AutoField(primary_key=True)
    reporter = models.ForeignKey(RegisteredUser, related_name = 'reported_concert', on_delete = models.DO_NOTHING)
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

