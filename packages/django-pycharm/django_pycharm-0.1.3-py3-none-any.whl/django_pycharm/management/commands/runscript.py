from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
import importlib.util


class Command(BaseCommand):
    help = 'Run specified Python script within Django context'

    def add_arguments(self, parser):
        parser.add_argument('filepath', type=str)

    def handle(self, *args, **options):
        if not Path(options["filepath"]).exists():
            raise CommandError(f"file not found: {options['filepath']}")

        spec = importlib.util.spec_from_file_location("__main__", options["filepath"])
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
