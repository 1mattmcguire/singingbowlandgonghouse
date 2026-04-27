"""
Sitemap configuration for Singing Bowl and Gong House.

Extend `url_names` to add more static pages to the sitemap.
"""
from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class StaticViewSitemap(Sitemap):
    """Sitemap for static pages with named URLs."""

    changefreq = "weekly"
    priority = 0.8

    def items(self):
        # Add more URL names here as you add pages (e.g. "main:about", "main:services")
        return [
            "main:home",
        ]

    def location(self, item):
        return reverse(item)
