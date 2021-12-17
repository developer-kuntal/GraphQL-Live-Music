from django.db import models
from bson import ObjectId
# Create your models here.
class Song(models.Model):
    # _id field must be added as a primary key(name must be: <_id>)
    # _id = models.BigAutoField(primary_key=True) 
    # __id = graphene.ID()
    _id = models.TextField(primary_key=True, max_length=30,default=ObjectId())
    # id = models.TextField()
    name = models.TextField(max_length=100,default=None)
    title = models.TextField(max_length=100,default=None)
    artist = models.TextField(max_length=100,default=None)
    album = models.TextField(max_length=50,default=None)
    year = models.CharField(max_length=10)
    duration_in_sec = models.IntegerField(default=None)
    bitrate = models.IntegerField(default=None)
    lyric = models.TextField(max_length=10000,default=None)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title