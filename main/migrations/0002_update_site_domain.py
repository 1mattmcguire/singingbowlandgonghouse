"""
Data migration to set the correct domain for the sitemap.
Sitemaps use django.contrib.sites to build absolute URLs.
"""
import os
from django.db import migrations


def update_site_domain(apps, schema_editor):
    Site = apps.get_model("sites", "Site")
    domain = os.getenv("SITE_DOMAIN", "singingbowlandgonghouse.com").strip()
    name = os.getenv("SITE_NAME", "Singing Bowl and Gong House").strip()
    Site.objects.update_or_create(
        id=1,
        defaults={"domain": domain, "name": name},
    )


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0001_initial"),
        ("sites", "0002_alter_domain_unique"),
    ]

    operations = [
        migrations.RunPython(update_site_domain, noop),
    ]
