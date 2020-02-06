from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
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

@login_required
def follower_following_list(request, operation):
    # If the operation(get from url) is as follows get context

    template = 'follow_system/follower_following_list.html'

    if operation == 'followers_list':

        f_relationship = FollowerSystem.objects.filter(
            friend=request.user
        )
        f_list = [f.current_user for f in f_relationship]

    elif operation == 'following_list':
        following, created = FollowerSystem.objects.get_or_create(
            current_user=request.user
        )

        f_list = following.friend.all()

    args = {'f_list': f_list}

    return render(request, template, args)
