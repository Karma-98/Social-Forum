from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

# Create your models here.


class ThreadPost(models.Model):

    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='threads_posts',
                             null=True)
    title = models.CharField(max_length=100, blank=False, null=True)
    text = models.TextField(blank=False, null=True)
    created_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField()

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        '''
        Food for thought: Will updating title change its url?
        '''
        self.slug = slugify(self.title)
        super(ThreadPost, self).save(*args, **kwargs)


class ThreadComment(models.Model):

    thread = models.ForeignKey(ThreadPost,
                               on_delete=models.SET_NULL,
                               related_name="thread_comments", null=True)
    text = models.TextField(blank=False, null=True)
    created_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User,
                             on_delete=models.SET_NULL,
                             related_name='comments',
                             null=True)

    def __str__(self):
        return self.text

