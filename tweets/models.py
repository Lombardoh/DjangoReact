import random
from django.db import models
from django.db.models.base import Model
from django.db.models.fields.files import ImageField
import random

class Tweet(models.Model):
    content = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='images/', blank=True, null=True)

    class Meta:
        ordering = ['-id']

    def serialize(self):
        return {
            "id": self.id,
            "content": self.content,
            "likes": random.randint(0,200)
        }