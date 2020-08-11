#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    ### DEBUG PRINTS FOR DEPLOYMENT BUG FIX ###
    print("env vars")
    print('DB_HOST', os.environ['DB_HOST'])
    print('DB_NAME', os.environ['DB_NAME'])
    print('DB_USER', os.environ['DB_USER'])
    print('DB_PASSWORD', os.environ['DB_PASSWORD'])
    ### DEBUG PRINTS FOR DEPLOYMENT BUG FIX ###
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pooling.settings')
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
