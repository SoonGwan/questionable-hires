const defaults = {retries:3};
export const origin = import.meta.url;
export function retries(options = {}) { return options.retries ?? defaults.retries; }
