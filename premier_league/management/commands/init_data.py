from django.core.management.base import BaseCommand
from premier_league.utils import initiate_db

class Command(BaseCommand):
    def handle(self, *args, **options):
        initiate_db()