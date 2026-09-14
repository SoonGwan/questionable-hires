def read_flag(env, name, default=False):
    value = env.get(name)
    if value is None:
        return default
    normalized = value.strip().lower()
    if normalized in {"true", "yes", "on", "1"}:
        return True
    if normalized in {"false", "no", "off", "0"}:
        return False
    raise ValueError("Invalid flag")
