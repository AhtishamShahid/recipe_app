"""
user models
"""

from django.db import models
from annoying.fields import AutoOneToOneField


class UserProfile(models.Model):
    """
    # https://stackoverflow.com/questions/10602071/following-users-like-twitter-in-django-how-would-you-do-it
    User profile model to make many to many recursive for user table
    """
    user = AutoOneToOneField('auth.user', on_delete='cascade')
    follows = models.ManyToManyField('UserProfile', related_name='followed_by')

    def __str__(self):
        """
        string representation of class
        :return:
        """
        return self.user.username  # pylint: disable=no-member
