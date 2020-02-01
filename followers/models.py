from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class FollowerSystem(models.Model):

    friend = models.ManyToManyField(User,
                                    related_name="following_system")

    current_user = models.ForeignKey(User,
                                     related_name="current_users",
                                     on_delete=models.CASCADE,
                                     blank=True,
                                     null=True)

    @classmethod
    def follow_action(cls, current_user, new_following):
        following, created = cls.objects.get_or_create(
            current_user=current_user
        )
        following.friend.add(new_following)
        # For many to many, if one to many just add in friend=new_following

    @classmethod
    def unfollow_action(cls, current_user, remove_following):
        following, created = cls.objects.get_or_create(
            current_user=current_user
        )
        following.friend.remove(remove_following)
        
