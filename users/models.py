# from django.db import models
# https://stackoverflow.com/questions/10602071/following-users-like-twitter-in-django-how-would-you-do-it
# from django.contrib.auth.models import User
#
#
# # Create your models here.
# class UserFollowsUser(models.Model):
#     follower = models.IntegerField('')


# class UserRelationship(models.Model):
#     types = models.ManyToManyField('User', blank=True,
#                                    related_name='user_relationships')
#     followee = models.ForeignKey('User', related_name='followee', on_delete='cascade')
#     follower = models.ForeignKey('User', related_name='follower', on_delete='cascade')
#
#     class Meta:
#         unique_together = ('followee', 'follower')

from django.db import models
from annoying.fields import AutoOneToOneField


class UserProfile(models.Model):
    user = AutoOneToOneField('auth.user', on_delete='cascade')
    follows = models.ManyToManyField('UserProfile', related_name='followed_by')

    def __str__(self):
        return self.user.username
