from django.contrib import admin
from .models import ThreadPost, ThreadComment


class CommentInline(admin.TabularInline):
    model = ThreadComment


class PostAdmin(admin.ModelAdmin):
    inlines = [
        CommentInline,
    ]


admin.site.register(ThreadPost, PostAdmin)
admin.site.register(ThreadComment)