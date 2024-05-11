from django.db import models


# Create your models here.
class Rooms(models.Model):
    name = models.CharField(max_length=50, unique=True)
    seats = models.IntegerField()
    projector = models.BooleanField()


class RoomsReservation(models.Model):
    date = models.DateField()
    room = models.ForeignKey(Rooms, on_delete=models.CASCADE)
    comment = models.TextField()

    class Meta:
        unique_together = ('date', 'room')
