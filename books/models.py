from typing_extensions import Required
from django.db import models
from bson import ObjectId

# Create your models here.
class Book(models.Model):
    id = models.CharField(primary_key=True, max_length=30, default=ObjectId())
    title = models.CharField(max_length=100,)
    excerpt = models.TextField(max_length=100,)

    def __str__(self):
        return self.title
