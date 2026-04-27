"""
Populate material, size, weight, note for existing instruments from descriptions.
Run: python manage.py populate_instrument_details
"""
from django.core.management.base import BaseCommand

from main.models import Instrument


# Extracted from instrument descriptions - map instrument name to details
INSTRUMENT_DETAILS = {
    "Old Buddha/Cham Bowl": {
        "material": "Seven metals (copper, tin, lead, mercury, iron, gold, silver)",
    },
    "Old Manipuree Bowl": {
        "material": "Seven metals (copper, tin, lead, mercury, iron, gold, silver)",
    },
    "Old Stand Bowl": {
        "material": "Seven metals (copper, tin, lead, mercury, iron, gold, silver)",
    },
    "Old Thado Bowl": {
        "material": "Seven metals (copper, tin, lead, mercury, iron, gold, silver)",
    },
    "Old Kopre Bowl": {
        "material": "Seven metals (copper, tin, lead, mercury, iron, gold, silver)",
    },
    "Old Jam Bowl": {
        "material": "Seven metals (copper, tin, lead, mercury, iron, gold, silver)",
    },
    "Old Ulta Bowl": {
        "material": "Seven metals (copper, tin, lead, mercury, iron, gold, silver)",
    },
    "New Handmade Singing Bowl": {
        "material": "Five metals (70% copper, 30% tin, iron, mercury, lead)",
    },
    "New etching and carving bowl": {
        "material": "Hand-etched and carved",
    },
    "Chakra Sets": {
        "material": "New handmade singing bowls",
        "weight": "9-10 kg",
        "note": "130Hz-246Hz (notes C-B)",
    },
    "Big Mother Bowls": {
        "material": "Five metals",
    },
    "Old Nipple Gong": {
        "material": "Traditional metal",
    },
    "New Nipple Gong": {
        "material": "Metal",
    },
    "TamTam Gong": {
        "material": "Seven metals",
    },
    "Handpan - Harmonic Series": {
        "material": "Steel",
        "note": "Harmonic series tuning",
    },
}


class Command(BaseCommand):
    help = "Populate material, size, weight, note from instrument descriptions"

    def handle(self, *args, **options):
        updated = 0
        for instrument in Instrument.objects.all():
            details = INSTRUMENT_DETAILS.get(instrument.name)
            if not details:
                continue
            changed = False
            for field in ("material", "size", "weight", "note"):
                value = details.get(field)
                if value and not getattr(instrument, field):
                    setattr(instrument, field, value)
                    changed = True
            if changed:
                instrument.save()
                updated += 1
                self.stdout.write(self.style.SUCCESS(f"  Updated: {instrument.name}"))

        self.stdout.write(self.style.SUCCESS(f"\nUpdated {updated} instruments."))
