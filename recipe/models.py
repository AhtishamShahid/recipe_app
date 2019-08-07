from django.db import models

# Create your models here.
from django.utils.timezone import now


class Ingredients(models.Model):
    title = models.CharField(max_length=30)
    pub_date = models.DateTimeField(default=now())


class Recipe(models.Model):
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=30)
    directions = models.CharField(max_length=600)
    ingredients = models.ManyToManyField(Ingredients)
    user_id = models.IntegerField(null=False, default=0)
    pub_date = models.DateTimeField(default=now())
