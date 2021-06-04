from django.db import models
from django.db.models.base import Model
from django.db.models.fields.files import ImageField

class Tweet(models.Model):
    content = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='imaegs/', blank=True, null=True)
