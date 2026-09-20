def page_limit(options):
    """Return the configured page limit without changing options."""
    value = options.get('limit')
    return 100 if value is None else value
