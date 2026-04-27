"""
Sitemap configuration for Singing Bowl and Gong House.

Lists every public, indexable page on the site so search engines can crawl
them. To add a new public page:

1. Add its URL name (e.g. ``main:gallery``) to ``StaticViewSitemap.items``.
2. Make sure the page does NOT emit ``<meta name="robots" content="noindex">``.

The sitemap is served at ``/sitemap.xml`` (configured in
``SingingBallAndGongHouse/urls.py``) and is also referenced from
``robots.txt``.
"""
from django.contrib.sitemaps import Sitemap
from django.urls import reverse

CANONICAL_DOMAIN = "singingbowlandgonghouse.com"


class StaticViewSitemap(Sitemap):
    """Sitemap for static pages with named URLs."""

    protocol = "https"

    PAGES = {
        "main:home": {"priority": 1.0, "changefreq": "weekly"},
        "main:about": {"priority": 0.8, "changefreq": "monthly"},
        "main:services": {"priority": 0.9, "changefreq": "weekly"},
        "main:products": {"priority": 0.9, "changefreq": "weekly"},
        "main:smiles": {"priority": 0.7, "changefreq": "weekly"},
        "main:booking": {"priority": 0.9, "changefreq": "monthly"},
        # NOTE: ``main:success`` is intentionally excluded from the sitemap.
        # It's a thank-you page shown only after a form submission and has no
        # SEO value. The template also emits ``<meta name="robots"
        # content="noindex, nofollow">`` so search engines won't index it even
        # if they discover the URL another way.
    }

    def items(self):
        return list(self.PAGES.keys())

    def location(self, item):
        return reverse(item)

    def priority(self, item):
        return self.PAGES[item]["priority"]

    def changefreq(self, item):
        return self.PAGES[item]["changefreq"]

    def get_domain(self, site=None):
        # Pin the sitemap to the canonical production domain regardless of
        # what's stored in django.contrib.sites' default Site row, so the
        # generated URLs are stable and SEO-correct.
        return CANONICAL_DOMAIN
