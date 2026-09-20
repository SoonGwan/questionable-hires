class Decoder {
  constructor() { this.pending = Buffer.alloc(0); }
  push(chunk) {
    this.pending = Buffer.concat([this.pending, chunk]);
    const frames = [];
    while (this.pending.length >= 2) {
      const size = this.pending.readUInt16BE(0);
      if (this.pending.length < 2 + size) break;
      this.pending = this.pending.subarray(2);
      frames.push(Buffer.from(this.pending.subarray(0, size)));
      this.pending = this.pending.subarray(size);
    }
    return frames;
  }
}
exports.Decoder = Decoder;
exports.origin = require('node:url').pathToFileURL(__filename).href;
