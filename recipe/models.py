"""
Application models list
"""
from django.db import models
from django.contrib.auth.models import User


class Ingredients(models.Model):
    """
    Ingredients model having m2m with recipe
    """
    title = models.CharField(max_length=30)
    pub_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Recipe(models.Model):
    """
    Recipe Model having m2m with ingredients
    """
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=30)
    directions = models.CharField(max_length=600)
    user = models.ForeignKey(User, related_name='recipe', on_delete=models.CASCADE)
    pub_date = models.DateTimeField(auto_now=True)
    ingredients = models.ManyToManyField(Ingredients)

    def __str__(self):
        return self.title
