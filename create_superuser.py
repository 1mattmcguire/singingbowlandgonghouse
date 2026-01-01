import os

import django
from django.contrib.auth import get_user_model


def main() -> None:
    """
    Idempotently create a Django superuser from environment variables.

    Required env vars:
      - DJANGO_SUPERUSER_USERNAME
      - DJANGO_SUPERUSER_EMAIL
      - DJANGO_SUPERUSER_PASSWORD
    """
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SingingBallAndGongHouse.settings")
    django.setup()

    username = os.getenv("DJANGO_SUPERUSER_USERNAME", "").strip()
    email = os.getenv("DJANGO_SUPERUSER_EMAIL", "").strip()
    password = os.getenv("DJANGO_SUPERUSER_PASSWORD", "").strip()

    if not username or not email or not password:
        raise SystemExit(
            "Missing required env vars. Set DJANGO_SUPERUSER_USERNAME, "
            "DJANGO_SUPERUSER_EMAIL, DJANGO_SUPERUSER_PASSWORD."
        )

    User = get_user_model()

    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(username=username, email=email, password=password)
        print("Superuser created successfully!")
    else:
        print("Superuser already exists.")


if __name__ == "__main__":
    main()

