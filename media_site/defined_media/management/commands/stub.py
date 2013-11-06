from django.core.management.base import BaseCommand, CommandError
from django.db import models
import defined_media.models as dm_models

class Command(BaseCommand):
    help='Rebuild the search database'

    def handle(self, *args, **options):
