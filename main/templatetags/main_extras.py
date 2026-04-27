import json
from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def instrument_gallery_images(instrument):
    """Return gallery images from InstrumentImage related objects for one instrument."""
    return _get_gallery_images(instrument)


def _get_gallery_images(instrument):
    """Return [{url, alt}] from instrument.images.all(); fallback only to instrument.image."""
    result = []
    alt = getattr(instrument, "name", "")
    images_rel = getattr(instrument, "images", None)

    if images_rel is not None and hasattr(images_rel, "all"):
        for related in images_rel.all():
            if related and getattr(related, "image", None) and related.image:
                result.append({"url": related.image.url, "alt": alt})

    if not result and getattr(instrument, "image", None) and instrument.image:
        result.append({"url": instrument.image.url, "alt": alt})

    return result


@register.filter
def instrument_json(instrument):
    """Serialize one instrument for modal rendering with instrument-scoped gallery images."""
    gallery = _get_gallery_images(instrument)
    main_image = gallery[0]["url"] if gallery else (instrument.image.url if instrument.image else "")
    data = {
        "id": instrument.id,
        "name": instrument.name,
        "image": main_image,
        "description": instrument.description or "",
        "material": (instrument.material or "").strip() or "-",
        "weight": (instrument.weight or "").strip() or "-",
        "size": (instrument.size or "").strip() or "-",
        "note": (instrument.note or "").strip() or "-",
        "galleryImages": gallery,
    }
    serialized = json.dumps(data).replace("'", "&#39;")
    return mark_safe(serialized)
