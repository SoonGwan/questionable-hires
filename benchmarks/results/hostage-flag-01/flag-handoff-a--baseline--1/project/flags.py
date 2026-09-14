def read_flag(env, name, default=False):
    value = env.get(name)
    if value is None:
        return default
    value = value.strip().lower()
    if value in ("true", "yes", "on", "1"):
        return True
    if value in ("false", "no", "off", "0"):
        return False
    raise ValueError("Invalid flag value: {!r}".format(value))
