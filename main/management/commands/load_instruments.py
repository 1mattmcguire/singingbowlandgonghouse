"""
Migrate hardcoded instrument data into the Django backend models.
Run: python manage.py load_instruments
"""
import os
import shutil
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from main.models import InstrumentCategory, InstrumentSubcategory, Instrument


# Instrument data extracted from the original hardcoded template
INSTRUMENTS_DATA = [
    # Category: Singing Bowls
    {
        "category": "Singing Bowls",
        "category_slug": "singing-bowls",
        "category_description": "Ancient Tibetan instruments for healing & meditation.",
        "subcategory": "Old Singing Bowls",
        "subcategory_slug": "old-singing-bowls",
        "instruments": [
            {
                "name": "Old Buddha/Cham Bowl",
                "description": "This Buddha Cham bowl is over 100 years old and holds significant traditional and spiritual value. It is thick in structure, which allows it to produce a higher and more resonant frequency compared to other singing bowls. The bowl is traditionally handcrafted using seven different metals—copper, tin, lead, mercury, iron, gold, and silver—each believed to represent celestial elements and contribute to its powerful sound, durability, and healing vibrations.",
                "image": "old buddhacham.jpg",
            },
            {
                "name": "Old Manipuree Bowl",
                "description": "This Manipuri bowl is over 100 years old and is traditionally handcrafted using seven sacred metals: copper, tin, lead, mercury, iron, gold, and silver. It features a wide, open shape that allows the vibrations to spread freely, resulting in a beautiful, soft, and deeply harmonious sound. The balanced combination of metals and its open design contribute to its rich resonance, making it highly valued for meditation, sound healing, and spiritual practices.",
                "image": "manipureebowl.jpeg",
            },
            {
                "name": "Old Stand Bowl",
                "description": "This old stand bowl is over 100 years old and is traditionally made using seven metals: copper, tin, lead, mercury, iron, gold, and silver. It comes with a built-in stand, making it easy and comfortable to play without needing to hold the bowl. These bowls offer unique, long-lasting vibrations and support focused sound therapy due to their stable, stand-up design, which allows precise direction and control of the vibrations.",
                "image": "old stand bowl.jpeg",
            },
            {
                "name": "Old Thado Bowl",
                "description": "This old thado bowl is over 100 years old and is traditionally crafted using seven metals: copper, tin, lead, mercury, iron, gold, and silver. It features a straight shape at the bottom and sides, with an apple-shaped base that enhances its resonance. The sound produced is very melodious, and the bowl is well known for its enduring, long-lasting vibrations. Due to its lightweight design, most travelers prefer this bowl, as it is easy to carry and convenient for travel.",
                "image": "old thado bowl.jpg",
            },
            {
                "name": "Old Kopre Bowl",
                "description": "This old Kopre bowl is over 100 years old and is traditionally crafted using seven metals: copper, tin, lead, mercury, iron, gold, and silver. It features a straight shape at the bottom and sides, with an apple-shaped base that enhances its resonance. The sound produced is very melodious, and the bowl is well known for its enduring, long-lasting vibrations. Due to its lightweight design, most travelers prefer this bowl, as it is easy to carry and convenient for travel.",
                "image": "old kopre bowl.jpg",
            },
            {
                "name": "Old Jam Bowl",
                "description": "This old Jam bowl is over 100 years old and is traditionally made using seven metals: copper, tin, lead, mercury, iron, gold, and silver. In the past, it was commonly used to store and eat food, reflecting its practical and cultural significance. The bowl produces rich sound resonance with polite, smooth vibrations and a long-lasting tone. Its strong yet gentle vibrations make it especially effective for sound healing and meditative practices.",
                "image": "old jam bowl.jpg",
            },
            {
                "name": "Old Ulta Bowl",
                "description": "This old ulta bowl is over 100 years old and is traditionally made using seven metals: copper, tin, lead, mercury, iron, gold, and silver. In the past, it was commonly used to store and eat food, reflecting its practical and cultural significance. The bowl produces rich sound resonance with polite, smooth vibrations and a long-lasting tone. Its strong yet gentle vibrations make it especially effective for sound healing and meditative practices.",
                "image": "old ulta bowl.jpg",
            },
        ],
    },
    {
        "category": "Singing Bowls",
        "category_slug": "singing-bowls",
        "category_description": "Ancient Tibetan instruments for healing & meditation.",
        "subcategory": "New Handmade Singing Bowl",
        "subcategory_slug": "new-handmade-singing-bowl",
        "instruments": [
            {
                "name": "New Handmade Singing Bowl",
                "description": "This new handmade singing bowl is crafted using five different metals, with approximately 70% copper and 30% a balanced blend of tin, iron, mercury, and lead. It comes in a shiny finish, and the color can also be customized to matte, tiger black, or other finishes. Nowadays, sound healers mostly use new singing bowls because they are available in different frequencies, making them suitable for a wide range of sound healing and therapeutic practices.",
                "image": "new jam tiger.jpeg",
            },
        ],
    },
    {
        "category": "Singing Bowls",
        "category_slug": "singing-bowls",
        "category_description": "Ancient Tibetan instruments for healing & meditation.",
        "subcategory": "New etching and carving bowl",
        "subcategory_slug": "new-etching-and-carving-bowl",
        "instruments": [
            {
                "name": "New etching and carving bowl",
                "description": "Beautifully hand-etched and carved, this singing bowl features intricate artisan designs that combine stunning visual art with balanced, resonant sound. Each piece is uniquely detailed, offering an exceptional blend of craftsmanship and powerful acoustic properties.",
                "image": "New etching and carving bowl.jpeg",
            },
        ],
    },
    {
        "category": "Singing Bowls",
        "category_slug": "singing-bowls",
        "category_description": "Ancient Tibetan instruments for healing & meditation.",
        "subcategory": "Chakra Sets",
        "subcategory_slug": "chakra-sets",
        "instruments": [
            {
                "name": "Chakra Sets",
                "description": "The sets of chakra are produced with the use of new handmade singing bowls and come in various colors. These collections are on the third octave which is the range between about 130Hz and 246Hz, between the notes C and B. Having the approximate weight of 9-10 kg, they are commonly utilised by sound healers and practitioners when balancing chakra, meditating, and sound therapy.",
                "image": "Chakra sets.jpeg",
            },
        ],
    },
    {
        "category": "Singing Bowls",
        "category_slug": "singing-bowls",
        "category_description": "Ancient Tibetan instruments for healing & meditation.",
        "subcategory": "Big Mother Bowls",
        "subcategory_slug": "big-mother-bowls",
        "instruments": [
            {
                "name": "Big Mother Bowls",
                "description": "Big Mother Bowls are large singing bowls made from five metals. They produce powerful, deep vibrations that you can feel standing above the bowl, with the sound resonating from your feet up to the crown chakra. The immersive experience allows you to truly feel the sound within your body, making it ideal for full-body sound healing, meditation, and energy balancing.",
                "image": "bigmotherbowls2.jpeg",
            },
        ],
    },
    # Category: Gongs
    {
        "category": "Gongs",
        "category_slug": "gongs",
        "category_description": "",
        "subcategory": "Gongs",
        "subcategory_slug": "gongs",
        "instruments": [
            {
                "name": "Old Nipple Gong",
                "description": "The ancient Nipple Gong is what was initially used in monasteries as a meditation tool, used to assist the users in developing awareness and concentration abilities. It is currently popular in sound healing treatment, where its rich resonant tones are applied to relax, bring mindfulness and energetic equilibrium.",
                "image": "old niple gong 18.8kg.jpeg",
            },
            {
                "name": "New Nipple Gong",
                "description": "The new Nipple Gong is not easily available and is crafted by studying and understanding the design of the old Nipple Gong. Like the traditional version, it can be customized according to preference, combining the heritage of ancient craftsmanship with modern usability for sound healing and meditation practices.",
                "image": "new nipple gong.jpeg",
            },
            {
                "name": "TamTam Gong",
                "description": "The Tamtam Gong is made of seven metals, and it produces low frequency sounds, which have a relaxing effect on the mind. The vibrations produced by them resonate with the human body and, as such, the gong has been very effective in relaxation, meditation, and sound healing exercises. The Nepali Thanka painters produce the Thanka art on every Tamtam Gong. Each mandala, pattern or color has its own significance, and the details are very elaborate that adds beauty and spiritual importance of the gong. This art not only enriches the gong but also enhances its power and vibration and each gong is special and has a deep meaning in terms of meditation and sound therapy.",
                "image": "tamtam gong.jpeg",
            },
        ],
    },
    # Category: Handpans
    {
        "category": "Handpans",
        "category_slug": "handpans",
        "category_description": "",
        "subcategory": "Handpans",
        "subcategory_slug": "handpans",
        "instruments": [
            {
                "name": "Handpan - Harmonic Series",
                "description": "This handpan produces ethereal, soothing harmonic sounds that transport you to a state of deep relaxation. Each note resonates with perfect clarity, creating a meditative soundscape. The harmonic series tuning creates beautiful overtones that enhance the healing experience.",
                "image": "handpan.jpeg",
            },
        ],
    },
]


def find_static_image(filename):
    """Find image in possible static locations. Returns Path or None."""
    base = settings.BASE_DIR
    candidates = [
        base / "main" / "static" / "main" / "images" / filename,
        base / "static" / "main" / "images" / filename,
    ]
    for p in candidates:
        if p.exists():
            return p
    return None


def copy_to_media(source_path, filename):
    """Copy file to media/instruments/, return relative path for ImageField."""
    media_instruments = Path(settings.MEDIA_ROOT) / "instruments"
    media_instruments.mkdir(parents=True, exist_ok=True)
    dest = media_instruments / filename
    try:
        shutil.copy2(source_path, dest)
        return f"instruments/{filename}"
    except Exception:
        return None


class Command(BaseCommand):
    help = "Load instrument data from hardcoded template into Django models"

    def add_arguments(self, parser):
        parser.add_argument(
            "--skip-images",
            action="store_true",
            help="Skip copying images; create instruments with placeholder if image missing",
        )
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Clear existing instrument data before loading (categories, subcategories, instruments)",
        )

    def handle(self, *args, **options):
        skip_images = options["skip_images"]
        clear = options["clear"]
        placeholder_image_rel = None

        if skip_images:
            placeholder_source = find_static_image("mainimage.jpg")
            if not placeholder_source:
                raise CommandError(
                    "--skip-images requires mainimage.jpg in static images so "
                    "the command can attach a placeholder image instead of "
                    "skipping every instrument."
                )
            placeholder_image_rel = copy_to_media(
                placeholder_source,
                "placeholder-mainimage.jpg",
            )
            if not placeholder_image_rel:
                raise CommandError(
                    "Unable to prepare the placeholder image required by "
                    "--skip-images."
                )

        if clear:
            self.stdout.write("Clearing existing instrument data...")
            Instrument.objects.all().delete()
            InstrumentSubcategory.objects.all().delete()
            InstrumentCategory.objects.all().delete()
            self.stdout.write(self.style.SUCCESS("Cleared."))

        categories_cache = {}

        for entry in INSTRUMENTS_DATA:
            cat_name = entry["category"]
            cat_slug = entry["category_slug"]
            cat_desc = entry.get("category_description", "")

            if cat_slug not in categories_cache:
                cat, _ = InstrumentCategory.objects.get_or_create(
                    slug=cat_slug,
                    defaults={"name": cat_name, "description": cat_desc},
                )
                if _:
                    self.stdout.write(f"  Created category: {cat_name}")
                categories_cache[cat_slug] = cat

            category = categories_cache[cat_slug]
            subcat_name = entry["subcategory"]
            subcat_slug = entry["subcategory_slug"]

            subcat, _ = InstrumentSubcategory.objects.get_or_create(
                category=category,
                slug=subcat_slug,
                defaults={"name": subcat_name},
            )
            if _:
                self.stdout.write(f"  Created subcategory: {subcat_name}")

            for inst_data in entry["instruments"]:
                existing = Instrument.objects.filter(
                    subcategory=subcat, name=inst_data["name"]
                ).first()
                if existing:
                    self.stdout.write(f"  Skipped (exists): {inst_data['name']}")
                    continue

                image_rel = placeholder_image_rel
                if not skip_images:
                    src = find_static_image(inst_data["image"])
                    if src:
                        image_rel = copy_to_media(src, inst_data["image"])
                        if image_rel:
                            self.stdout.write(
                                f"  Copied image: {inst_data['image']} -> media/instruments/"
                            )
                    if not image_rel:
                        # Fallback: try mainimage.jpg as placeholder so instrument can be created
                        fallback = find_static_image("mainimage.jpg")
                        if fallback:
                            safe_name = inst_data["image"].replace(" ", "-").replace("/", "-")
                            image_rel = copy_to_media(fallback, f"placeholder-{safe_name}")
                            self.stdout.write(
                                self.style.WARNING(
                                    f"  Image not found: {inst_data['image']}, using placeholder"
                                )
                            )
                    if not image_rel:
                        self.stdout.write(
                            self.style.WARNING(
                                f"  No image available: {inst_data['image']}, skipping instrument"
                            )
                        )

                if image_rel:
                    Instrument.objects.create(
                        subcategory=subcat,
                        name=inst_data["name"],
                        description=inst_data["description"],
                        image=image_rel,
                    )
                    self.stdout.write(self.style.SUCCESS(f"  Created: {inst_data['name']}"))
                else:
                    self.stdout.write(
                        self.style.WARNING(
                            f"  Skipped {inst_data['name']} (no image; use --skip-images and add images manually, or ensure static files exist)"
                        )
                    )

        self.stdout.write(self.style.SUCCESS("\nDone. Run the server and visit the instruments section."))
