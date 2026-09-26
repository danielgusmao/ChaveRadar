from pathlib import Path

from django.conf import settings


def app_meta(request):
    version_file = Path(settings.BASE_DIR) / "VERSION"
    try:
        version = version_file.read_text(encoding="utf-8").strip()
    except OSError:
        version = "0.0.0"

    environment = "Online" if getattr(settings, "DATABASE_URL", "") else "Local"
    return {
        "app_version": version,
        "app_environment": environment,
    }
