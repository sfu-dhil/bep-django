from django.db import models
from django.utils.safestring import mark_safe
from solo.models import SingletonModel
from django_advance_thumbnail import AdvanceThumbnailField

# abstract Models

# Models (load order matters)
class HomePage(SingletonModel):
    heading = models.CharField(default='Books in English Parishes')
    content = models.TextField()

    # relationships

    # write tracking fields
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'bep_config_home_page'
        verbose_name = 'Home Page'

    def __str__(self):
        return 'Home Page'

class AboutPage(SingletonModel):
    heading = models.CharField(default='Books in English Parishes')
    content = models.TextField()

    # relationships

    # one-to-many team_members via TeamMember Model
    # one-to-many content_blocks via ContentBlock Model


    # write tracking fields
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'bep_config_about_page'
        verbose_name = 'About Page'

    def __str__(self):
        return 'About Page'

class AboutContentBlock(models.Model):
    heading = models.CharField()
    content = models.TextField()
    image = models.ImageField(
        upload_to='images/',
        help_text=mark_safe('Please use <u><a href="https://developer.mozilla.org/en-US/docs/Web/Media/Formats/Image_types" target="_blank">standard web image types</a></u>. PNG, JPEG, and WebP are recommended.'),
        verbose_name='Content Block Image',
    )
    thumbnail = AdvanceThumbnailField(
        source_field='image',
        upload_to='thumbnails/',
        null=True,
        blank=True,
        size=(600, 400),
    )
    order = models.PositiveIntegerField(
        default=0,
        blank=False,
        null=False,
    )

    # relationships
    about_page = models.ForeignKey(
        AboutPage,
        related_name='content_blocks',
        on_delete=models.CASCADE,
    )

    # write tracking fields
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'bep_config_about_content_block'
        ordering = ['order']

    def __str__(self):
        return self.heading


class TeamMember(models.Model):
    name = models.CharField()
    profile = models.TextField()
    image = models.ImageField(
        upload_to='images/',
        help_text=mark_safe('Please use <u><a href="https://developer.mozilla.org/en-US/docs/Web/Media/Formats/Image_types" target="_blank">standard web image types</a></u>. PNG, JPEG, and WebP are recommended.'),
        verbose_name='Profile Picture',
    )
    thumbnail = AdvanceThumbnailField(
        source_field='image',
        upload_to='thumbnails/',
        null=True,
        blank=True,
        size=(150, 150),
    )
    order = models.PositiveIntegerField(
        default=0,
        blank=False,
        null=False,
    )

    # relationships
    about_page = models.ForeignKey(
        AboutPage,
        related_name='team_members',
        on_delete=models.CASCADE,
    )

    # write tracking fields
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'bep_config_team_member'
        ordering = ['order']

    def __str__(self):
        return self.name