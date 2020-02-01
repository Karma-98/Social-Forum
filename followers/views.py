from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.views import generic
from .models import FollowerSystem

# Create your views here.


@login_required
def add_or_remove_friend(request, operation, slug):

    new_follower = User.objects.get(userprofile__slug=slug)

    if operation == 'add':
        FollowerSystem.follow_action(request.user, new_follower)

    if operation == 'remove':
        FollowerSystem.unfollow_action(request.user, new_follower)

    return redirect('profile')

# @login_required
# def friend_list(request, operation, slug):
#     # If the operation(get from url) is as follows get context

#     if operation == 'followers_list':
#         try:
#             followers_list = FollowerSystem.objects.get(
#                 current_user=request.user
#                 ).friends.all()

#         except FollowerSystem.DoesNotExist:
#             followers_list = 'You have no followers yet'

#     if operation == 'following_list':
#         following_list = FollowerSystem.objects.filter(
#             friends=request.user
#         ).all()

    

    

