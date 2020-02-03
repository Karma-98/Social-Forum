from django.views import generic
from .forms import RegistrationForm, ProfileForm
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import views as authviews
from django.shortcuts import redirect, get_object_or_404

from django.contrib.auth.models import User
from .models import UserProfile
from threads.models import ThreadPost, ThreadComment
from followers.models import FollowerSystem


class RegistrationView(generic.CreateView):
    form_class = RegistrationForm
    success_url = reverse_lazy('login')
    template_name = 'accounts/registration.html'

    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('profile')
        return super().dispatch(*args, **kwargs)


class LoginView(authviews.LoginView):

    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('profile')
        return super().dispatch(*args, **kwargs)


class ProfileView(LoginRequiredMixin, generic.DetailView):
    login_url = reverse_lazy('login')
    template_name = 'accounts/profile.html'

    def get_object(self):
        return self.request.user

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)

        current_user = self.request.user

        following, created = FollowerSystem.objects.get_or_create(
            current_user=current_user
        )

        context['number_of_following'] = following.friend.count()

        context['number_of_followers'] = FollowerSystem.objects.filter(
            friend=self.request.user
        ).count()

        return context


class ProfileUpdateView(LoginRequiredMixin, generic.UpdateView):
    login_url = reverse_lazy('login')
    form_class = ProfileForm
    template_name = 'accounts/profile-update.html'

    def get_initial(self):
        return {'bio': self.request.user.userprofile.bio}

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        return reverse('profile')


class PasswordExtResetView(authviews.PasswordResetView):
    html_email_template_name = 'accounts/password_reset_email.html'
    subject_template_name = 'accounts/password_reset_subject.txt'


class PasswordResetCompleted(authviews.PasswordResetConfirmView):
    success_url = reverse_lazy('password_reset_completed')


class AccountDeleteView(LoginRequiredMixin, generic.DeleteView):
    success_url = reverse_lazy('login')
    template_name = 'accounts/account-delete.html'

    def get_object(self):
        return get_object_or_404(User, pk=self.request.user.pk)


class OtherProfileView(generic.DetailView):
    template_name = 'accounts/other_profile.html'
    context_object_name = "userprofile"

    def get_object(self, **kwargs):
        return get_object_or_404(
            UserProfile, slug=self.kwargs.get('slug')
        )

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)

        context['num_started_threads'] = User.objects.get(
            userprofile__slug=self.kwargs.get('slug')).threads_posts.count()

        context['num_comments'] = User.objects.get(
            userprofile__slug=self.kwargs.get('slug')).comments.count()

        if self.request.user.is_authenticated:
            context['is_following'] = FollowerSystem.objects.filter(
                current_user=self.request.user, friend__userprofile__slug=self.kwargs.get('slug')
                ).exists()

        # try:
        #     context['number_of_following'] = FollowerSystem.objects.get(
        #         current_user__username=self.kwargs.get('slug')
        #         ).friend.count()

        # except FollowerSystem.DoesNotExist:
        #     context['number_of_following'] = 0

        # context['number_of_following'] = FollowerSystem.objects.filter(
        #         current_user__username=self.kwargs.get('slug')
        #         ).count()

        other_user = User.objects.get(userprofile__slug=self.kwargs.get('slug'))

        following, created = FollowerSystem.objects.get_or_create(
            current_user=other_user
        )

        context['number_of_following'] = following.friend.count()

        context['number_of_followers'] = FollowerSystem.objects.filter(
            friend__userprofile__slug=self.kwargs.get('slug')
            ).count()

        return context
