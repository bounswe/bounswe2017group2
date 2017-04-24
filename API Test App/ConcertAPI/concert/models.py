# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import django as dj
from django.db import models

from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles

LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted((item, item) for item in get_all_styles())

# Concert class, represents the a concert event
class Concert(models.Model):
    
    # creation time of the concert object
    created = models.DateTimeField(auto_now_add=True)
    
    # Artist of the concert
    artist = models.TextField(blank=False, default='')
    
    # Location of the concert
    location = models.TextField(blank=False, default='')
    
    # Date of the concert
    date= models.DateField(blank=False, default=dj.utils.timezone.now)
    
    # Min ticket price, 0 by default
    minprice = models.IntegerField(default=0)
    
    # Max ticket price, 0 by default
    maxprice = models.IntegerField(default=0)
    
    class Meta:
        ordering = ('created',)
