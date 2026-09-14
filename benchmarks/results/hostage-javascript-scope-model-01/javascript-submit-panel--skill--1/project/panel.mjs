export class SubmitPanel {
  pending = false;

  async submit(save, signal) {
    if (this.pending) return undefined;
    this.pending = true;
    try {
      return await save(signal);
    } finally {
      this.pending = false;
    }
  }
}
