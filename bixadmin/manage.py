#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

bixengine_path = os.environ.get('BIXENGINE_PATH')
if bixengine_path and bixengine_path not in sys.path:
    sys.path.insert(0, bixengine_path)

def main():
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bixadmin.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == "__main__":
    main()
