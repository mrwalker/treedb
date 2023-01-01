from django.contrib import admin

from trees.models import Tree, Site


@admin.register(Tree)
class TreeAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'description', 'site', 'species', 'created', 'updated'
    )


@admin.register(Site)
class SiteAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'owner', 'created', 'updated')
