def options(config):
    seconds = config.get('timeout_seconds')
    milliseconds = int(float(seconds) * 1000) if seconds is not None else int(config.get('timeout_ms', 1000))
    return {'timeout_ms': milliseconds, 'attempts': int(config.get('attempts', 3))}
