from django.db import models

# Create your models here.
class Concert(models.Model):
    concert_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length= 150)"""!""""
    artist = models.CharField(max_length= 50)"""!""""
    """location -implemented in location --ONE TO MANY""" """!"""
    """tags -implemented in tag --MANY TO MANY""" """!"""
    date_time = models.DateTimeField()"""!""""
    description =  models.CharField(max_length=2000,allow_blank=True)"""!""""
    price_min = models.IntegerField()"""!""""
    price_max = models.IntegerField()"""!""""
    """attenders -will be implemented in User --MANY TO MANY"""
    """ratings -implemented in Rating"""
    """concertReports -implemented in Report --ONE TO MANY"""
    class Meta:
        unique_together = ("artist", "date_time")
    
class Tag(models.Model):
    tag_id = models.AutoField(primary_key=True)
    concerts = models.ManyToManyField(Concert, related_name = 'tags') """might need on_delete = DO_NOTHING but couldn't find on_delete as a parameter in its documentation"""
    value = models.CharField(max_length=50)

class Report(models.Model): """NEEDS THINKING"""
    report_id = models.AutoField(primary_key=True)
    reporter = models.ForeignKey(User, related_name = 'reported_concert', on_delete = models.DO_NOTHING)
    concert = models.ForeignKey(Concert, related_name = 'reports',on_delete = models.CASCADE)
    content = models.CharField() """ <---------------------------------------------------------------- NEED TO HAVE A STRUCTURE FOR REPORT"""
    
    
class User(models.Model): """NEEDS IMPLEMENTING / THINKING"""
    
    
class Location(models.Model):
    location_id = models.AutoField(primary_key=True)
    venue = models.CharField(max_length = 200)
    coordinates = models.CharField() """ GOOGLE API !"""
    concert = models.ForeignKey(Concert, related_name = 'location', on_delete = models.DO_NOTHING); """<--- If we store venues and will give """
    class Meta:
        unique_together = ("venue", "coordinates")

class Rating(models.Model):
    rating_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, related_name = 'concert_ratings', on_delete = models.CASCADE)
    concert = models.ForeignKey(Concert, related_name = 'ratings', on_delete = models.CASCADE)
    rating = models.IntegerField();
