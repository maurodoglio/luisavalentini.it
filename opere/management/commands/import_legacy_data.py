"""
Management command to import data from the legacy Django dumpdata JSON backup.
Filters and loads only the 'opere' app models (Opera, Mostra) and auth User data.
"""

import json

from django.core.management.base import BaseCommand

from opere.models import Mostra, Opera


class Command(BaseCommand):
    help = 'Import data from the legacy db_backup.json (dumpdata format)'

    def add_arguments(self, parser):
        parser.add_argument(
            'json_file',
            help='Path to the legacy db_backup.json file',
        )

    def handle(self, *args, **options):
        json_file = options['json_file']

        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        mostre_count = 0
        opere_count = 0

        for item in data:
            model = item.get('model', '')
            fields = item.get('fields', {})

            if model == 'opere.mostra':
                Mostra.objects.update_or_create(
                    pk=item['pk'],
                    defaults={
                        'name': fields.get('name', ''),
                        'slug': fields.get('slug', ''),
                        'content': fields.get('content', ''),
                        'published': fields.get('published', False),
                        'type': fields.get('type', '1'),
                        'beginning': fields.get('beginning'),
                    },
                )
                mostre_count += 1

            elif model == 'opere.opera':
                Opera.objects.update_or_create(
                    pk=item['pk'],
                    defaults={
                        'title': fields.get('title', ''),
                        'slug': fields.get('slug', ''),
                        'published': fields.get('published', True),
                        'content': fields.get('content', ''),
                        'image': fields.get('image', ''),
                        'thumb': fields.get('thumb', ''),
                        'creation_year': fields.get('creation_year', ''),
                        'typology': fields.get('typology', 'S'),
                    },
                )
                opere_count += 1

        self.stdout.write(self.style.SUCCESS(
            f'Imported {mostre_count} mostre and {opere_count} opere.'
        ))
