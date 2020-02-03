from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path('<operation>/<slug>/', views.add_or_remove_friend, name="add_or_remove_friend"),
    path('<operation>/', views.follower_following_list, name="follower_following_list")
]