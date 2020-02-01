from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path('login/', views.LoginView.as_view(template_name="accounts/login.html"), name="login"),  # noqa
    path('logout/', auth_views.LogoutView.as_view(), name="logout"),
    path('signup/', views.RegistrationView.as_view(), name="signup"),
    path('profile/', views.ProfileView.as_view(), name="profile"),
    path('profile/update/', views.ProfileUpdateView.as_view(), name="profile_update"), # noqa
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name="accounts/password_change.html"), name="password_change"), # noqa
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name="accounts/password_change_done.html"), name="password_change_done"), # noqa
    path('password_reset/', views.PasswordExtResetView.as_view(template_name="accounts/password_reset.html") ,name="password_reset"), # noqa
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_done.html"), name="password_reset_done"), # noqa
    path('password_reset_confirmation/<uidb64>/<token>/', views.PasswordResetCompleted.as_view(template_name="accounts/password_reset_confirm.html"), name="password_reset_confirmation"), # noqa
    path('password_reset/complete/', auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'), name='password_reset_completed'), # noqa
    path('delete_account/', views.AccountDeleteView.as_view(), name='account_delete'), # noqa
    path('<slug>/', views.OtherProfileView.as_view(), name='other_profile'),
]
