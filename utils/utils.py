# utils/utils.py
"""
General utility functions for the application.
Keep authentication logic in utils/auth.py.
"""

def format_currency(value):
    """Format a numeric value as USD currency string."""
    try:
        return f"${float(value):,.2f}"
    except (ValueError, TypeError):
        return "$0.00"

def format_date(dt):
    """Format a datetime object as ISO string."""
    if dt:
        return dt.isoformat()
    return None