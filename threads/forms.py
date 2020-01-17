from django import forms
from .models import ThreadPost, ThreadComment


class ThreadPostForm(forms.ModelForm):

    class Meta:
        model = ThreadPost
        fields = ('title', 'text', )


class ThreadCommentForm(forms.ModelForm):

    class Meta:
        model = ThreadComment
        fields = ('text', 'thread', 'user', )
        widgets = {
            'thread': forms.HiddenInput(),
            'user': forms.HiddenInput(),
        }
