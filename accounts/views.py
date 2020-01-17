from django.views import generic
from .forms import RegistrationForm, ProfileForm
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import views as authviews
from django.shortcuts import redirect, get_object_or_404
from django.db.models import Count

from django.contrib.auth.models import User
from .models import UserProfile
from threads.models import ThreadPost, ThreadComment

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

    def get_object(self, **kwargs):
        return get_object_or_404(
            UserProfile, slug=self.kwargs.get('slug')
        )

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['num_started_threads'] = User.objects.get(username=self.kwargs.get('slug')).threads_posts.count()
        context['num_comments'] = User.objects.get(username=self.kwargs.get('slug')).comments.count()
        return context
