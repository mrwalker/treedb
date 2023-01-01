from django.conf import settings
from django.db import models


class Tree(models.Model):
    created = models.DateTimeField(null=False, auto_now_add=True)
    updated = models.DateTimeField(null=False, auto_now=True)

    title = models.CharField(null=False, blank=False, max_length=255)
    description = models.TextField(null=False, blank=False)

    # Location
    site = models.ForeignKey('Site', on_delete=models.CASCADE)
    site_tree_id = models.CharField(null=False, blank=False, max_length=255)
    location_lat = models.DecimalField(null=False, blank=False, max_digits=9, decimal_places=6)
    location_lon = models.DecimalField(null=False, blank=False, max_digits=9, decimal_places=6)

    # Tree info
    species = models.URLField(null=False, blank=False)
    diameter_at_breast_height = models.PositiveIntegerField(null=False, blank=False)
    # condition

    # Maintenance plan
    # Photos

    class Meta:
        unique_together = ('site', 'site_tree_id')

    def __str__(self):
        return f'{self.id} - ({self.site_tree_id}) {self.title}: {self.description}'


class Site(models.Model):
    created = models.DateTimeField(null=False, auto_now_add=True)
    updated = models.DateTimeField(null=False, auto_now=True)

    title = models.CharField(null=False, blank=False, max_length=255)
    description = models.TextField(null=False, blank=False)

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.id} - {self.title}: {self.description}'
