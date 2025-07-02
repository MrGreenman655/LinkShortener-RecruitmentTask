from django.db import models


# Create your models here.
class Link(models.Model):
    url = models.CharField(max_length=512, verbose_name="Link")
    short_url_hash = models.CharField(
        max_length=512,
        verbose_name="Short link",
        help_text="Only last letters without host",
        null=True,
        blank=True,
    )
