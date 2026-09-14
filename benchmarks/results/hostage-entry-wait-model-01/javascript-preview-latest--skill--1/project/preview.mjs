export class PreviewLoader {
  state = { status: 'idle', value: null, error: null };
  #latestRequest;

  async load(key, fetchBytes, decode, signal) {
    const request = this.#latestRequest = {};
    this.state = { status: 'loading', value: this.state.value, error: null };
    try {
      const bytes = await fetchBytes(key, signal);
      const value = await decode(bytes, signal);
      if (request === this.#latestRequest) {
        this.state = { status: 'ready', value, error: null };
      }
      return value;
    } catch (error) {
      if (request === this.#latestRequest) {
        this.state = { status: 'error', value: this.state.value, error };
      }
      throw error;
    }
  }
}
