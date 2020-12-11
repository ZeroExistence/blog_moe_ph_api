from django.db import models
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from django.contrib.auth.models import AbstractUser
from django.contrib.sites.models import Site
from django.contrib.sites.managers import CurrentSiteManager


class User(AbstractUser):
    pass


# Create your models here.

def upload_media(instance, filename):
    return '{0}/{1}'.format(instance.id, filename)


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.CharField(
        max_length=50,
        blank=True,
        editable=False,
        unique=True
    )
    sites = models.ManyToManyField(Site)

    objects = models.Manager()
    on_site = CurrentSiteManager()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['name']


class Image(models.Model):
    original = models.ImageField(upload_to=upload_media)
    caption = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )


class Post(models.Model):
    title = models.CharField(max_length=100, unique=True)
    slug = models.CharField(
        max_length=100,
        blank=True,
        editable=False,
        unique=True
    )
    intro = models.CharField(
        max_length=200,
        null=True,
        blank=True
    )
    image = models.ForeignKey(
        Image,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    content = RichTextField()
    tag = models.ManyToManyField(Tag)
    date = models.DateField()
    sites = models.ManyToManyField(Site)

    objects = models.Manager()
    on_site = CurrentSiteManager()

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['date', 'title']
