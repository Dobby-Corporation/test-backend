from django.db import models

# Create your models here.

class Person(models.Model):
    vk_id = models.IntegerField(unique=True)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    photo = models.URLField()