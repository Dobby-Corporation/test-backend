from django.db import models

# Create your models here.

class User(models.Model):
    tg_id = models.IntegerField(unique=True)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    username = models.CharField(max_length=64)
    photo_url = models.URLField(null=True)
