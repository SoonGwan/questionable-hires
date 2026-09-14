export class PreviewLoader {
  state = { status: 'idle', value: null, error: null };
  #request;
  async load(key, fetchBytes, decode, signal) {
    const request = this.#request = {};
    this.state = { status: 'loading', value: this.state.value, error: null };
    try {
      const bytes = await fetchBytes(key, signal);
      const value = await decode(bytes, signal);
      if (this.#request === request) {
        this.state = { status: 'ready', value, error: null };
      }
      return value;
    } catch (error) {
      if (this.#request === request) {
        this.state = { status: 'error', value: this.state.value, error };
      }
      throw error;
    }
  }
}
