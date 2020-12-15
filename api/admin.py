from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Post, Tag, Image

# Register your models here.


class PostModelAdmin(admin.ModelAdmin):
    list_filter = ('sites',)
    list_display = ('title', 'in_sites',)


class TagModelAdmin(admin.ModelAdmin):
    list_filter = ('sites',)
    list_display = ('name', 'in_sites')


admin.site.register(User, UserAdmin)
admin.site.register(Post, PostModelAdmin)
admin.site.register(Tag, TagModelAdmin)
admin.site.register(Image)
