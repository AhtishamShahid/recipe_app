from django.db import models

# Create your models here.
from django.utils.timezone import now


class Ingredients(models.Model):
    title = models.CharField(max_length=30)
    pub_date = models.DateTimeField(default=now())

    def __str__(self):
        return self.title


class Recipe(models.Model):
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=30)
    directions = models.CharField(max_length=600)
    user = models.ForeignKey('auth.User', related_name='recipe', on_delete=models.CASCADE)
    pub_date = models.DateTimeField(default=now())
    ingredients = models.ManyToManyField(Ingredients)

    def __str__(self):
        return self.title
