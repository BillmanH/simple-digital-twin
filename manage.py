#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

def main():
    """Run administrative tasks."""
    if os.environ.get('ENVIRONMENT') != 'prod':
        print('Running in Development environment')
        print("** you need to route to `http://localhost:8000/` for the active directory components to work **")
    settings_module = 'app.production' if 'WEBSITE_HOSTNAME' in os.environ else 'app.settings'
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
