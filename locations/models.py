from django.db import models


# Create your models here.
class Location(models.Model):
    id = models.AutoField(primary_key=True)
    # latitude
    lat = models.FloatField(null=False)
    # longitude
    lon = models.FloatField(null=False)
    # location
    loc = models.TextField(null=False)

    def __str__(self):
        return self.loc
