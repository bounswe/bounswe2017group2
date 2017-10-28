from django.db import models
from django.contrib.auth.models import AbstractUser

# Models in our Database.

class RegisteredUser(AbstractUser): #NEEDS IMPLEMENTING / THINKING
    '''
    '''
    #user_id = models.AutoField(primary_key=True)
    age = models.IntegerField()
    #location = models.CharField(max_length=40)
    #concerts = models.ManyToManyField(Concert, related_name= 'users')

class Location(models.Model):
    location_id = models.AutoField(primary_key=True)
    # venue and coordinates should be retrieved from Google API.
    # charfields are placeholders for now.
    venue = models.CharField(max_length = 200)
    coordinates = models.CharField(max_length=200)

    class Meta:
        unique_together = ("venue", "coordinates")

class Concert(models.Model):
    concert_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length= 150)
    artist = models.CharField(max_length= 50)
    location = models.ForeignKey(Location, related_name = 'concerts', on_delete = models.CASCADE,  null=True);

    #location -implemented in location --ONE TO MANY
    #tags -implemented in tag --MANY TO MANY
    #date_time = models.DateTimeField()
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
    #owner_id = models.ForeignKey(RegisteredUser, related_name = 'comments', on_delete = models.CASCADE , null = True) ----------> Needs session functionality
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
    owner = models.ForeignKey(RegisteredUser, related_name = 'concert_ratings', on_delete = models.CASCADE)
    concert = models.ForeignKey(Concert, related_name = 'ratings', on_delete = models.CASCADE)
    rating = models.IntegerField();
