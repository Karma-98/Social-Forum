from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.defaultfilters import slugify
from tinymce.models import HTMLField
from imagekit.models import ProcessedImageField
from imagekit.processors import SmartResize
# Create your models here.


class UserProfile(models.Model):
    ''' User description'''
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userprofile')
    bio = HTMLField(blank=True, null=True)
    photo = ProcessedImageField(upload_to='accounts',
                                format='JPEG',
                                options={'quality': 85},
                                blank=True,
                                null=True,
                                processors=[SmartResize(250, 250), ])
    slug = models.SlugField(blank=False, null=True)

    @property
    def default_image(self):
        if self.photo:
            return self.photo.url
        else:
            default_image_url = '/media/accounts/default.jpg'
            return default_image_url

    def __str__(self):
        return f'@{self.user.username}'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.user.username)
        super(UserProfile, self).save(*args, **kwargs)


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    '''
    John fills up the registration form and press the submit button.
    The csrf token is validated and form data is sent and populates the
    User model. Also a signal is sent by the User model and recieves by
    the UserProfile model creating an instance of the UserProfile with
    default values.
    '''
    if created:
        UserProfile.objects.create(user=instance)
    else:
        instance.userprofile.save()  # can use get_or_create method then use add() 
