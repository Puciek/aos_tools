from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.models import Count

from data.models import *
from data.tasks import fetch_pairings_for_event


class Command(BaseCommand):
    help = "Fetch pairings for events from BCP"

    def add_arguments(self, parser):
        parser.add_argument(
            "--celery",
            action="store_true",
            dest="celery",
            default=False,
            help="Use celery to fetch lists",
        )

    def handle(self, *args, **options):
        headers = settings.BCP_HEADERS
        events = (
            Event.objects.filter(source=BCP)
            .annotate(pairings_count=Count("pairings"))
            .exclude(pairings_count__gt=2)
        )
        self.stdout.write(f"Fetching data for {events.count()} events")
        tasks = []
        for event in events:
            if options["celery"]:
                tasks.append(fetch_pairings_for_event.delay(event.id))
            else:
                fetch_pairings_for_event(event.id)

        if options["celery"]:
            self.stdout.write(f"Started {len(tasks)} tasks")
        else:
            self.stdout.write(f"Finished fetching pairings")
