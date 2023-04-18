from django.db import models


class Location(models.Model):
    """
    Location model  #
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    latitude = models.FloatField()
    longitude = models.FloatField()


class Hospital(models.Model):
    """
    Hospital model  
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    beds_available = models.IntegerField()
    location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name
