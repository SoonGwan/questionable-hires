def options(config):
    return {'timeout_ms': int(config.get('timeout_ms', 1000)),
            'attempts': int(config.get('attempts', 3))}
