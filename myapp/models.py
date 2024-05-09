from django.db import models

# Create your models here.
class Rooms(models.Model):
    name = models.CharField(max_length=50)
    seats = models.IntegerField()
    projector = models.BooleanField()
