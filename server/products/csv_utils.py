"""Utilities for handling CSV file operations."""
import os
import subprocess
from django.conf import settings
from django.core.management.base import CommandError


def get_default_csv_path():
    """Get the path to the default CSV file."""
    base_dir = str(settings.BASE_DIR)
    return os.path.join(base_dir, 'data', 'receipts_data.csv')


def download_default_csv():
    """Download the default CSV from Google Sheets."""
    base_dir = str(settings.BASE_DIR)
    script_path = os.path.join(base_dir, 'download_default_csv.sh')
    
    if not os.path.exists(script_path):
        raise CommandError(f'Download script not found at {script_path}')
    
    result = subprocess.run(['bash', script_path], capture_output=True, text=True, cwd=base_dir)
    if result.returncode != 0:
        raise CommandError(f'Failed to download default CSV: {result.stderr}')
    
    csv_path = get_default_csv_path()
    if not os.path.exists(csv_path):
        raise CommandError(f'Downloaded CSV not found at {csv_path}')
    
    return csv_path


def resolve_csv_path(csv_path=None):
    if csv_path is None:
        return download_default_csv()
    
    if not os.path.exists(csv_path):
        raise CommandError(f'CSV file not found: {csv_path}')
    
    return csv_path

