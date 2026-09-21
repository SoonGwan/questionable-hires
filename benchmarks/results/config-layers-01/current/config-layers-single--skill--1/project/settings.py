def resolve(defaults, environment, overrides):
    result = dict(defaults)
    for layer in (environment, overrides):
        for key, value in layer.items():
            if value is not None:
                result[key] = value
    return result
