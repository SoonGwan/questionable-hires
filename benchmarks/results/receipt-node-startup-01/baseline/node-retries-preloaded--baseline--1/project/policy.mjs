const defaults = globalThis.RUNTIME_DEFAULTS;
void defaults.retries;
export const origin = import.meta.url;
export function retries(options = {}) { return options.retries ?? defaults.retries; }
