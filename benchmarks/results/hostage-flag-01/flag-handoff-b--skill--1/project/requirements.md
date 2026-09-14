read_flag(env, name, default=False) reads a supplied mapping, never global
environment state. Values are strings or None; default is a bool. Missing/None
returns default unchanged. Strip surrounding whitespace and ignore letter case.
true/yes/on/1 mean True; false/no/off/0 mean False. Empty/whitespace-only and every
other string raise ValueError; error wording is unspecified. Never mutate env.
worker_options uses TRACE with default False; preserve its retries=3 and API.
Do not add accepted spellings, imports of external packages or global settings.
