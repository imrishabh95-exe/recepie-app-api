import time

from django.db import connections
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    '''Django command to pause execution untill database is avaialable'''


    def handle(self, *arge, **options):
        self.stdout.write('Waiting for database...')
        db_conn = None
        while not db_conn:
            try:
                db_conn = connections['default']
            except OperationalError:
                self.stdout.write('Database unavailabe, waiting 1 sec')
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS('Database available!'))
