from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User


class RegistrationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name',
        'email', 'password1', 'password2',) # noqa

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        email = self.cleaned_data['email']
        username = self.cleaned_data['username']

        if email and User.objects.filter(email=email).exclude(username=username).exists(): # noqa
            raise forms.ValidationError(u'Email addresses must be unique.')
        return cleaned_data


class ProfileForm(UserChangeForm):

    bio = forms.CharField(widget=forms.Textarea)
    photo = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name',
        'email',) # noqa

    def save(self, *args, **kwargs):
        instance = super(ProfileForm, self).save(*args, **kwargs)
        profile = instance.userprofile
        profile.bio = self.cleaned_data['bio']
        profile.photo = self.cleaned_data['photo']
        profile.save()
        return instance

    def clean(self):
        cleaned_data = super(ProfileForm, self).clean()
        email = self.cleaned_data['email']
        username = self.cleaned_data['username']

        if email and User.objects.filter(email=email).exclude(username=username).exists(): # noqa
            raise forms.ValidationError(u'Email addresses must be unique.')
        return cleaned_data
