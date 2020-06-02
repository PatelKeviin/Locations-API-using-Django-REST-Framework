from django.db import models


# creating the model
class Setting(models.Model):
    # name
    name = models.TextField(max_length=30, null=False)
    # type
    type = models.TextField(max_length=30, null=False)
    # value
    value = models.TextField(max_length=100, null=False)

    def __str__(self):
        return self.name
