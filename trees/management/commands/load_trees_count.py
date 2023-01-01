import csv

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from trees.models import Site, Tree


class Command(BaseCommand):
    help = 'Load inventories from Trees Count app CSV export'

    site_field_map = {
        'title': 'InventoryName',
        'description': 'Landuse',
    }

    tree_field_map = {
        'title': 'SpeciesCN',
        'description': 'Notes',
        'site_tree_id': 'TreeID',
        'location_lat': 'Latitude',
        'location_lon': 'Longitude',
        'species': 'SpeciesCN',
        'diameter_at_breast_height': 'TreeDBH',
    }

    tree_species_urls = {
        'American elm': 'https://texastreeplanting.tamu.edu/Display_Onetree.aspx?tid=99',
        'Ashe juniper': 'https://en.wikipedia.org/wiki/Juniperus_ashei',
        'Cedar elm': 'https://texastreeplanting.tamu.edu/Display_Onetree.aspx?tid=100',
        'Chinese pistache': 'https://texastreeplanting.tamu.edu/Display_Onetree.aspx?tid=63',
        'Netleaf white oak': 'https://texastreeplanting.tamu.edu/Display_Onetree.aspx?tid=86',
        'Sugarberry': 'https://texastreeplanting.tamu.edu/Display_Onetree.aspx?tid=13',
        'Texas live oak': 'https://texastreeplanting.tamu.edu/Display_Onetree.aspx?tid=88',
        'Texas persimmon': 'https://texastreeplanting.tamu.edu/Display_Onetree.aspx?tid=26',
        'Texas red oak': 'https://texastreeplanting.tamu.edu/Display_Onetree.aspx?tid=75',
        'Weeping willow': 'https://en.wikipedia.org/wiki/Salix_babylonica',
    }


    def add_arguments(self, parser):
        parser.add_argument('filepath')

    def handle(self, *args, **kwargs):
        filepath = kwargs['filepath']
        owner = get_user_model().objects.get(email='matt.r.walker@gmail.com')

        with open(filepath) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                site = self._get_or_create_site(row, owner)
                self._get_or_create_tree(row, site)

    def _get_or_create_site(self, row, owner):
        site, created = Site.objects.get_or_create(
            title=row[self.site_field_map['title']],
            defaults={
                'description': row[self.site_field_map['description']],
                'owner': owner,
            }
        )
        return site

    def _get_or_create_tree(self, row, site):
        tree, created = Tree.objects.get_or_create(
            site=site,
            site_tree_id=row[self.tree_field_map['site_tree_id']],
            defaults={
                'title': row[self.tree_field_map['title']],
                'description': row[self.tree_field_map['description']],
                'location_lat': row[self.tree_field_map['location_lat']],
                'location_lon': row[self.tree_field_map['location_lon']],
                'species': self.tree_species_urls[row[self.tree_field_map['species']]],
                'diameter_at_breast_height': row[self.tree_field_map['diameter_at_breast_height']],
            }
        )
        return tree
