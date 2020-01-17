from django.urls import path
from . import views

urlpatterns = [
    path('thread-details/<slug>/', views.ThreadDetailView.as_view(), name='thread_detail'),
    path('new_thread/', views.ThreadCreateView.as_view(), name='thread_create'),
    path('update_thread/<slug>/', views.ThreadUpdateView.as_view(), name='thread_update'),
    path('delete_thread/<slug>/', views.ThreadDeleteView.as_view(), name='thread_delete'),
]